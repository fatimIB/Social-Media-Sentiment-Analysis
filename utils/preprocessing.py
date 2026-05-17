"""
Text preprocessing utilities.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean raw text before sentiment analysis.

    Steps:
    - Lowercase conversion
    - URL removal
    - Mention removal
    - Hashtag cleaning
    - Punctuation removal
    - Extra spaces removal
    """

    if not text or not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove mentions
    text = re.sub(r"@\w+", "", text)

    # Remove hashtags symbol only
    text = re.sub(r"#(\w+)", r"\1", text)

    # Remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove standalone numbers
    text = re.sub(r"\b\d+\b", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()