"""Tokopedia URL generation utilities."""

from urllib.parse import quote

from .config import TOKOPEDIA_BASE_URL, REFERENCE_DATA


def generate_tokopedia_url(search_query: str) -> str:
    """
    Generate a Tokopedia search URL from a search query.

    Args:
        search_query: The Indonesian search query.

    Returns:
        Full Tokopedia search URL.
    """
    encoded_query = quote(search_query, safe="")
    return f"{TOKOPEDIA_BASE_URL}{encoded_query}"


def find_similar_in_reference(query: str, category: str | None = None) -> str | None:
    """
    Find a similar item in reference data for better search terms.

    Args:
        query: The search query to match.
        category: Optional category to filter by.

    Returns:
        Better search query if found, None otherwise.
    """
    query_lower = query.lower()

    # Search in accessories first (they have direct queries)
    for acc in REFERENCE_DATA.get("looks", {}).get("accessories", []):
        if acc.get("query", "").lower() == query_lower:
            return acc["query"]
        if query_lower in acc.get("name_ua", "").lower():
            return acc["query"]

    # Search in looks
    for look_type in ["male_unisex", "female"]:
        for look in REFERENCE_DATA.get("looks", {}).get(look_type, []):
            for search in look.get("searches", []):
                if search.get("query", "").lower() == query_lower:
                    return search["query"]

    return None


def get_accessory_suggestions(count: int = 3) -> list[dict]:
    """
    Get random accessory suggestions from reference data.

    Args:
        count: Number of suggestions to return.

    Returns:
        List of accessory dictionaries.
    """
    accessories = REFERENCE_DATA.get("looks", {}).get("accessories", [])
    return accessories[:count] if accessories else []
