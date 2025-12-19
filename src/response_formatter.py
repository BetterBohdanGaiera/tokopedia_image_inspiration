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


def split_message(text: str, max_length: int = 4096) -> list[str]:
    """
    Split a long message into chunks at logical breakpoints.

    Splits at double newlines (between items) to keep related content together.

    Args:
        text: The text to split.
        max_length: Maximum length per chunk (default: Telegram's 4096 limit).

    Returns:
        List of message chunks.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by double newlines (between items)
    paragraphs = text.split("\n\n")

    for para in paragraphs:
        # If adding this paragraph exceeds limit, start new chunk
        if current_chunk and len(current_chunk) + len(para) + 2 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
