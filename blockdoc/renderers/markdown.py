"""
BlockDoc Markdown Renderer

Converts BlockDoc documents to Markdown
"""

from datetime import datetime


def render_to_markdown(article):
    """
    Render a BlockDoc document to Markdown

    Args:
        article (dict): The article object from a BlockDoc document

    Returns:
        str: Markdown representation
    """
    if not article or "blocks" not in article or not isinstance(article["blocks"], list):
        raise ValueError("Invalid article structure")

    markdown = [f"# {article['title']}", ""]

    # Add metadata if present
    if article.get("metadata"):
        metadata = article["metadata"]

        if metadata.get("author"):
            markdown.append(f"> Author: {metadata['author']}")

        if metadata.get("publishedDate"):
            try:
                date = datetime.fromisoformat(metadata["publishedDate"].replace("Z", "+00:00"))
                markdown.append(f"> Published: {date.strftime('%a %b %d %Y')}")
            except (ValueError, AttributeError):
                # If date parsing fails, just use the raw value
                markdown.append(f"> Published: {metadata['publishedDate']}")

        if metadata.get("tags") and isinstance(metadata["tags"], list) and metadata["tags"]:
            markdown.append(f"> Tags: {', '.join(metadata['tags'])}")

        markdown.append("")

    # Render each block
    for block in article["blocks"]:
        markdown.append(render_block_to_markdown(block))
        markdown.append("")  # Add a blank line after each block

    return "\n".join(markdown)


def render_block_to_markdown(block):
    """
    Render a single block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation of the block
    """
    block_type = block.get("type", "")

    if block_type == "text":
        return render_text_block_to_markdown(block)
    elif block_type == "heading":
        return render_heading_block_to_markdown(block)
    elif block_type == "image":
        return render_image_block_to_markdown(block)
    elif block_type == "code":
        return render_code_block_to_markdown(block)
    elif block_type == "list":
        return render_list_block_to_markdown(block)
    elif block_type == "quote":
        return render_quote_block_to_markdown(block)
    elif block_type == "embed":
        return render_embed_block_to_markdown(block)
    elif block_type == "divider":
        return "---"
    else:
        return f"[Unknown block type: {block_type}]"


def render_text_block_to_markdown(block):
    """
    Render a text block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation
    """
    # Text content is already in markdown format
    return block.get("content", "")


def render_heading_block_to_markdown(block):
    """
    Render a heading block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation
    """
    level = block.get("level", 2)
    content = block.get("content", "")

    # Ensure level is between 1-6
    valid_level = min(max(int(level), 1), 6)
    hashtags = "#" * valid_level

    return f"{hashtags} {content}"


def render_image_block_to_markdown(block):
    """
    Render an image block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation
    """
    url = block.get("url", "")
    alt = block.get("alt", "")
    caption = block.get("caption")

    markdown = f"![{alt}]({url})"

    if caption:
        markdown += f"\n*{caption}*"

    return markdown


def render_code_block_to_markdown(block):
    """
    Render a code block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation
    """
    language = block.get("language", "")
    content = block.get("content", "")

    return f"```{language}\n{content}\n```"


def render_list_block_to_markdown(block):
    """
    Render a list block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation
    """
    items = block.get("items", [])
    # Support both snake_case (Python style) and camelCase (JS style)
    list_type = block.get("list_type", block.get("listType", "unordered"))

    if not items or not isinstance(items, list):
        return "[Invalid list items]"

    markdown_items = []
    for i, item in enumerate(items):
        if list_type == "ordered":
            markdown_items.append(f"{i + 1}. {item}")
        else:
            markdown_items.append(f"- {item}")

    return "\n".join(markdown_items)


def render_quote_block_to_markdown(block):
    """
    Render a quote block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation
    """
    content = block.get("content", "")
    attribution = block.get("attribution")

    # Prefix each line with '> '
    markdown = "\n".join([f"> {line}" for line in content.split("\n")])

    if attribution:
        markdown += f"\n>\n> — {attribution}"

    return markdown


def render_embed_block_to_markdown(block):
    """
    Render an embed block to Markdown

    Args:
        block (dict): Block data

    Returns:
        str: Markdown representation
    """
    url = block.get("url", "")
    caption = block.get("caption")
    # Support both snake_case (Python style) and camelCase (JS style)
    embed_type = block.get("embed_type", block.get("embedType", "generic"))

    markdown = f"[{embed_type or 'Embedded content'}: {url}]({url})"

    if caption:
        markdown += f"\n*{caption}*"

    return markdown
