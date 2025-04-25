"""
BlockDoc HTML Renderer

Converts BlockDoc documents to HTML
"""

import re

from markdown import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

from blockdoc.utils.sanitize import sanitize_html, sanitize_url


def render_to_html(article):
    """
    Render a BlockDoc document to HTML

    Args:
        article (dict): The article object from a BlockDoc document

    Returns:
        str: HTML representation
    """
    if not article or "blocks" not in article or not isinstance(article["blocks"], list):
        raise ValueError("Invalid article structure")

    html = [
        '<article class="blockdoc-article">',
        f'<h1 class="blockdoc-title">{sanitize_html(article["title"])}</h1>',
    ]

    # Render each block
    for block in article["blocks"]:
        html.append(render_block(block))

    html.append("</article>")

    return "\n".join(html)


def render_block(block):
    """
    Render a single block to HTML

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation of the block
    """
    block_id = block.get("id", "")
    block_type = block.get("type", "")

    # Wrapper with block ID and type as data attributes
    open_wrapper = (
        f'<div class="blockdoc-block blockdoc-{block_type}" data-block-id="{block_id}" data-block-type="{block_type}">'
    )
    close_wrapper = "</div>"

    if block_type == "text":
        content = render_text_block(block)
    elif block_type == "heading":
        content = render_heading_block(block)
    elif block_type == "image":
        content = render_image_block(block)
    elif block_type == "code":
        content = render_code_block(block)
    elif block_type == "list":
        content = render_list_block(block)
    elif block_type == "quote":
        content = render_quote_block(block)
    elif block_type == "embed":
        content = render_embed_block(block)
    elif block_type == "divider":
        content = render_divider_block()
    else:
        content = f"<p>Unknown block type: {block_type}</p>"

    return f"{open_wrapper}{content}{close_wrapper}"


def render_text_block(block):
    """
    Render a text block

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation
    """
    # Use markdown to convert markdown to HTML
    return markdown(block.get("content", ""))


def render_heading_block(block):
    """
    Render a heading block

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation
    """
    level = block.get("level", 2)
    content = block.get("content", "")

    # Ensure level is between 1-6
    valid_level = min(max(int(level), 1), 6)

    return f"<h{valid_level}>{sanitize_html(content)}</h{valid_level}>"


def render_image_block(block):
    """
    Render an image block

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation
    """
    url = sanitize_url(block.get("url", ""))
    alt = sanitize_html(block.get("alt", ""))
    caption = block.get("caption")

    img_html = f'<img src="{url}" alt="{alt}" class="blockdoc-image" />'

    if caption:
        img_html += f'<figcaption class="blockdoc-caption">{sanitize_html(caption)}</figcaption>'
        return f'<figure class="blockdoc-figure">{img_html}</figure>'

    return img_html


def render_code_block(block):
    """
    Render a code block

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation
    """
    language = block.get("language", "")
    content = block.get("content", "")

    # Use pygments for syntax highlighting
    try:
        if language and language != "plain":
            lexer = get_lexer_by_name(language)
        else:
            lexer = guess_lexer(content)

        highlighted_code = highlight(content, lexer, HtmlFormatter())
    except (ClassNotFound, Exception):
        highlighted_code = sanitize_html(content)

    return f"""
    <pre class="blockdoc-pre">
      <code class="blockdoc-code {f"language-{language}" if language else ""}">
{highlighted_code}
      </code>
    </pre>
    """


def render_list_block(block):
    """
    Render a list block

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation
    """
    items = block.get("items", [])
    # Support both snake_case (Python style) and camelCase (JS style)
    list_type = block.get("list_type", block.get("listType", "unordered"))

    if not items or not isinstance(items, list):
        return "<p>Invalid list items</p>"

    tag = "ol" if list_type == "ordered" else "ul"

    items_html = []
    for item in items:
        rendered_item = markdown(item)
        # Remove paragraph tags that markdown adds by default
        rendered_item = rendered_item.replace("<p>", "").replace("</p>", "")
        items_html.append(f"<li>{rendered_item}</li>")

    return f'<{tag} class="blockdoc-list blockdoc-list-{list_type}">{"".join(items_html)}</{tag}>'


def render_quote_block(block):
    """
    Render a quote block

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation
    """
    content = block.get("content", "")
    attribution = block.get("attribution")

    html = f'<blockquote class="blockdoc-quote">{markdown(content)}</blockquote>'

    if attribution:
        html += f'<cite class="blockdoc-attribution">{sanitize_html(attribution)}</cite>'

    return html


def render_embed_block(block):
    """
    Render an embed block

    Args:
        block (dict): Block data

    Returns:
        str: HTML representation
    """
    url = sanitize_url(block.get("url", ""))
    caption = block.get("caption")
    # Support both snake_case (Python style) and camelCase (JS style)
    embed_type = block.get("embed_type", block.get("embedType", "generic"))

    if embed_type == "youtube":
        # Extract YouTube video ID
        video_id = extract_youtube_id(url)
        if video_id:
            embed_html = f"""
            <div class="blockdoc-embed-container">
              <iframe 
                width="560" 
                height="315" 
                src="https://www.youtube.com/embed/{video_id}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
              </iframe>
            </div>
            """
        else:
            embed_html = "<p>Invalid YouTube URL</p>"
    elif embed_type == "twitter":
        embed_html = f"""
        <div class="blockdoc-embed blockdoc-twitter">
          <blockquote class="twitter-tweet">
            <a href="{url}"></a>
          </blockquote>
          <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        </div>
        """
    else:
        # Generic embed with iframe
        embed_html = f"""
        <div class="blockdoc-embed">
          <iframe 
            src="{url}" 
            frameborder="0" 
            width="100%" 
            height="400"
            allowfullscreen>
          </iframe>
        </div>
        """

    if caption:
        embed_html += f'<figcaption class="blockdoc-caption">{sanitize_html(caption)}</figcaption>'
        return f'<figure class="blockdoc-figure">{embed_html}</figure>'

    return embed_html


def render_divider_block():
    """
    Render a divider block

    Returns:
        str: HTML representation
    """
    return '<hr class="blockdoc-divider" />'


def extract_youtube_id(url):
    """
    Extract YouTube video ID from URL

    Args:
        url (str): YouTube URL

    Returns:
        str or None: YouTube video ID or None if invalid
    """
    # Check for youtu.be format
    youtu_be_match = re.match(r"https?://youtu\.be/([a-zA-Z0-9_-]+)", url)
    if youtu_be_match:
        return youtu_be_match.group(1)

    # Check for youtube.com format
    youtube_match = re.match(r"https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)", url)
    if youtube_match:
        return youtube_match.group(1)

    return None
