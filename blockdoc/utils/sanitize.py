"""
BlockDoc HTML Sanitization

Provides utilities for sanitizing HTML content
"""

import html
import re


def sanitize_html(html_content):
    """
    Simple HTML sanitizer to prevent XSS

    Args:
        html_content (str): HTML content to sanitize

    Returns:
        str: Sanitized HTML
    """
    if not html_content:
        return ""

    return html.escape(str(html_content))


def sanitize_url(url):
    """
    Sanitize a URL for safe embedding

    Args:
        url (str): URL to sanitize

    Returns:
        str: Sanitized URL
    """
    if not url:
        return ""

    # Only allow http and https protocols
    if re.match(r"^https?:\/\/", url, re.IGNORECASE):
        return url
    elif url.startswith("//"):
        return f"https:{url}"
    elif ":" not in url:
        # Relative URLs are considered safe
        return url

    # Default to empty for potentially unsafe protocols
    return ""
