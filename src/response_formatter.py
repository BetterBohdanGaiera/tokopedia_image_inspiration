"""Response formatter for Telegram bot messages."""

import random
from typing import Any

from .tokopedia_search import generate_tokopedia_url

# Fun greetings for responses
GREETINGS = [
    "Ох ти і загнув! Окей, ось що знайшов:",
    "Ого, який лук! Тримай посилання:",
    "Нічо так! Ось що підібрав:",
    "О, бачу стиль! Лови:",
    "Круто! Ось твої луки:",
    "Файний вибір! Тримай:",
    "Вау, це щось! Ось посилання:",
    "Зрозумів завдання! Лови:",
]


def format_analysis_response(analysis_result: dict[str, Any]) -> str:
    """
    Format the Gemini analysis result into a Telegram message.

    All responses are in UKRAINIAN with Indonesian Tokopedia URLs.

    Args:
        analysis_result: The parsed analysis from Gemini.

    Returns:
        Formatted message string in Ukrainian.
    """
    if "error" in analysis_result:
        return (
            "Ой, щось пішло не так при аналізі фото! "
            f"Помилка: {analysis_result.get('error', 'Невідома помилка')}"
        )

    people = analysis_result.get("people", [])

    if not people:
        return (
            "Не вдалося знайти одяг на цьому фото. "
            "Спробуй надіслати інше фото з людьми у чіткому одязі!"
        )

    lines = []

    # Use LLM-generated greeting if available, fallback to random
    greeting = analysis_result.get("greeting_ua") or random.choice(GREETINGS)
    lines.append(greeting)
    lines.append("")

    # Format each person's items
    for i, person in enumerate(people):
        if len(people) > 1:
            description = person.get("description_ua", f"Людина {i + 1}")
            lines.append(f"**{description}**")
            lines.append("")

        items = person.get("items", [])
        for item in items:
            name_ua = item.get("name_ua", "Невідомий предмет")
            search_query = item.get("search_query_id", "")

            if search_query:
                url = generate_tokopedia_url(search_query)
                lines.append(f"{name_ua}")
                lines.append(url)
                lines.append("")

        if len(people) > 1 and i < len(people) - 1:
            lines.append("")

    return "\n".join(lines).strip()


def format_start_message() -> str:
    """
    Format the welcome message for /start command.

    Returns:
        Welcome message in Ukrainian.
    """
    return "Допомагаю знайти луки на Tokopedia. Кидай фото - кину посилання!"


def format_error_message(error: str | None = None) -> str:
    """
    Format an error message.

    Args:
        error: Optional specific error message.

    Returns:
        Error message in Ukrainian.
    """
    base_message = "Ой, сталася помилка!"
    if error:
        return f"{base_message} {error}"
    return f"{base_message} Спробуй ще раз пізніше."


def split_message_for_caption(
    text: str,
    caption_limit: int = 900,
    message_limit: int = 4096
) -> tuple[str, list[str]]:
    """
    Split text into caption and follow-up messages.

    Keeps item name + URL pairs together (they're separated by single newline).
    Splits at double newlines (between items).

    Args:
        text: The full response text.
        caption_limit: Max chars for photo caption.
        message_limit: Max chars for text messages.

    Returns:
        Tuple of (caption, list of follow-up messages).
    """
    if len(text) <= caption_limit:
        return text, []

    # Split by double newlines to get logical blocks (greeting, items, etc.)
    # Each item block contains: "item name\nURL"
    blocks = text.split("\n\n")

    caption_blocks = []
    remaining_blocks = []
    current_length = 0

    for i, block in enumerate(blocks):
        block_length = len(block) + (2 if caption_blocks else 0)  # +2 for "\n\n"

        if current_length + block_length <= caption_limit:
            caption_blocks.append(block)
            current_length += block_length
        else:
            # This and all remaining blocks go to follow-up messages
            remaining_blocks = blocks[i:]
            break

    caption = "\n\n".join(caption_blocks)

    # Split remaining into message chunks
    follow_up_messages = []
    if remaining_blocks:
        current_chunk = ""
        for block in remaining_blocks:
            block_length = len(block) + (2 if current_chunk else 0)

            if current_chunk and len(current_chunk) + block_length > message_limit:
                follow_up_messages.append(current_chunk.strip())
                current_chunk = block
            else:
                if current_chunk:
                    current_chunk += "\n\n" + block
                else:
                    current_chunk = block

        if current_chunk:
            follow_up_messages.append(current_chunk.strip())

    return caption, follow_up_messages
