"""Gemini Pro image analysis module for clothing identification."""

import base64
import json
import logging
from typing import Any

from google import genai
from google.genai import types

from .config import GEMINI_API_KEY, GEMINI_MODEL, REFERENCE_DATA

logger = logging.getLogger(__name__)

# Initialize the client globally
_client = None


def _get_client() -> genai.Client:
    """Get or create the Gemini client."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def _build_reference_examples() -> str:
    """Build reference examples from loaded JSON data."""
    examples = []

    # Add examples from male/unisex looks
    for look in REFERENCE_DATA.get("looks", {}).get("male_unisex", [])[:3]:
        for search in look.get("searches", [])[:1]:
            examples.append(f"- {look['name']} -> \"{search['query']}\"")

    # Add examples from female looks
    for look in REFERENCE_DATA.get("looks", {}).get("female", [])[:3]:
        for search in look.get("searches", [])[:1]:
            examples.append(f"- {look['name']} -> \"{search['query']}\"")

    # Add accessory examples
    for acc in REFERENCE_DATA.get("looks", {}).get("accessories", [])[:5]:
        examples.append(f"- {acc['name_ua']} -> \"{acc['query']}\"")

    return "\n".join(examples)


ANALYSIS_PROMPT = """Ти - експерт з моди для БОЖЕВІЛЬНОЇ ПЛЯЖНОЇ ВЕЧІРКИ (Beach Trash Party, Zatoka vibes, Verka Serduchka style).

Проаналізуй це зображення та визнач ВСІ предмети одягу на кожній людині.

ВАЖЛИВО:
- Відповідай УКРАЇНСЬКОЮ мовою
- Пошукові запити для Tokopedia - ІНДОНЕЗІЙСЬКОЮ
- Шукай ДЕШЕВІ, ТРЕШОВІ, БОЖЕВІЛЬНІ варіанти (для одноразової вечірки!)
- Пріоритет: дешевизна > якість

Для кожного предмета надай:
1. Назва українською (коротка, 3-5 слів максимум, смішна)
2. Пошуковий запит для Tokopedia (ІНДОНЕЗІЙСЬКОЮ!)
3. Категорія (top, bottom, accessory, footwear, headwear)

КРИТИЧНО для пошукових запитів - ЗАВЖДИ додавай МАКСИМУМ деталей:
- Колір (putih, hitam, merah, biru, pink, hijau, kuning, orange, ungu, coklat, abu-abu, emas, perak)
- Візерунок/принт (motif bunga, polos, garis-garis, kotak-kotak, motif abstrak, motif hewan)
- Тип/стиль (lengan pendek, lengan panjang, ketat, longgar, oversized, crop top)
- Матеріал якщо видно (katun, denim, kulit, sutra, rajut)
- "murah" в кінці для дешевих варіантів

Приклади ПРАВИЛЬНИХ детальних запитів:
- Біла сорочка з квітами → "Kemeja pria putih motif bunga lengan pendek murah"
- Чорні шорти → "Celana pendek pria hitam polos murah"
- Рожева майка → "Tank top wanita pink polos murah"
- Джинсова куртка синя → "Jaket denim biru pria murah"

Приклади з референсних даних:
{examples}

Поверни ТІЛЬКИ валідний JSON без markdown форматування:
{{
  "people": [
    {{
      "description_ua": "Опис людини українською",
      "items": [
        {{"name_ua": "Назва українською", "search_query_id": "Indonesian query with color+pattern+style+murah", "category": "top/bottom/accessory/footwear/headwear"}}
      ]
    }}
  ]
}}
"""


def analyze_image(image_bytes: bytes) -> dict[str, Any]:
    """
    Analyze an image to identify clothing items.

    Args:
        image_bytes: The image data as bytes.

    Returns:
        Dictionary containing identified clothing items and crazy ideas.
    """
    client = _get_client()

    # Build prompt with reference examples
    examples = _build_reference_examples()
    prompt = ANALYSIS_PROMPT.format(examples=examples)

    # Convert image bytes to base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Create the content with image
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                ),
            ]
        )
    ]

    logger.info(f"Analyzing image with Gemini model: {GEMINI_MODEL}")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
    )

    # Parse the response
    response_text = response.text.strip()

    # Remove markdown code blocks if present
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    try:
        result = json.loads(response_text)
        logger.info(f"Successfully parsed response with {len(result.get('people', []))} people detected")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        logger.error(f"Raw response: {response_text}")
        # Return a fallback structure
        return {
            "people": [],
            "crazy_ideas": [],
            "error": f"Failed to parse response: {str(e)}",
            "raw_response": response_text
        }
