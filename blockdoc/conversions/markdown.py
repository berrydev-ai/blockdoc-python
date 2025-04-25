"""Markdown to BlockDoc Converter

Utilities for converting Markdown documents to BlockDoc format
"""

import re
import uuid
from typing import Any, Dict, List, Optional

from blockdoc.core.block import Block
from blockdoc.core.document import BlockDocDocument


def markdown_to_blockdoc(
    markdown_text: str,
    title: str = "Untitled Document",
    metadata: Optional[Dict[str, Any]] = None,
) -> BlockDocDocument:
    """
    Convert a Markdown document to BlockDoc format

    Args:
        markdown_text (str): The markdown content to convert
        title (str, optional): Document title. Defaults to "Untitled Document".
        metadata (Dict, optional): Optional document metadata. Defaults to None.

    Returns:
        BlockDocDocument: A BlockDoc document generated from the markdown
    """
    if metadata is None:
        metadata = {}

    # Create a new BlockDoc document
    doc = BlockDocDocument({"title": title, "metadata": metadata})

    # Extract the title from markdown if available and not explicitly provided
    if title == "Untitled Document":
        first_line = markdown_text.strip().split("\n")[0]
        if first_line.startswith("# "):
            extracted_title = first_line[2:].strip()
            if extracted_title:
                doc.article["title"] = extracted_title
                # Remove the title line from the markdown
                markdown_text = "\n".join(markdown_text.strip().split("\n")[1:]).strip()

    # Split the markdown into blocks
    blocks = split_markdown_into_blocks(markdown_text)

    # Convert each block to a BlockDoc block and add to document
    for block in blocks:
        blockdoc_block = convert_block_to_blockdoc(block)
        if blockdoc_block:
            doc.add_block(blockdoc_block)

    return doc


def split_markdown_into_blocks(markdown_text: str) -> List[Dict[str, str]]:
    """
    Split a markdown document into discrete blocks for conversion

    Args:
        markdown_text (str): Markdown content to split

    Returns:
        List[Dict[str, str]]: List of block data with type and content
    """
    if not markdown_text.strip():
        return []

    lines = markdown_text.split("\n")
    blocks = []
    current_block = None

    # Various state tracking variables
    in_code_block = False
    code_lang = ""
    in_list = False
    list_items = []
    list_type = ""
    current_list_indent = 0
    in_quote = False
    quote_lines = []
    quote_has_attribution = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()

        # Handle code blocks
        if stripped_line.startswith("```"):
            if not in_code_block:
                # Start of code block
                if current_block:
                    blocks.append(current_block)
                    current_block = None

                in_code_block = True
                code_lang = stripped_line[3:].strip() or "plain"
                current_block = {"type": "code", "content": "", "language": code_lang}
            else:
                # End of code block
                in_code_block = False
                blocks.append(current_block)
                current_block = None
            i += 1
            continue
        elif in_code_block:
            # Inside code block - preserve all formatting including empty lines
            if current_block["content"]:
                current_block["content"] += "\n"
            current_block["content"] += line
            i += 1
            continue

        # Handle horizontal rules
        if re.match(r"^(---|\*\*\*|___)\s*$", stripped_line) and not in_quote and not in_list:
            if current_block:
                blocks.append(current_block)
            blocks.append({"type": "divider", "content": ""})
            current_block = None
            i += 1
            continue

        # Handle headings (ATX style: # Heading)
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped_line)
        if heading_match and not in_quote and not in_list:
            if current_block:
                blocks.append(current_block)

            level = len(heading_match.group(1))
            content = heading_match.group(2).strip()
            blocks.append({"type": "heading", "content": content, "level": level})
            current_block = None
            i += 1
            continue

        # Handle Setext-style headings (Heading\n=====)
        if i + 1 < len(lines) and not in_quote and not in_list and current_block and current_block["type"] == "text":
            next_line = lines[i + 1].strip()
            if re.match(r"^=+$", next_line):
                # Level 1 heading
                content = current_block["content"].strip()
                blocks.pop()  # Remove the text block we just added
                blocks.append({"type": "heading", "content": content, "level": 1})
                current_block = None
                i += 2  # Skip the underline
                continue
            elif re.match(r"^-+$", next_line):
                # Level 2 heading
                content = current_block["content"].strip()
                blocks.pop()  # Remove the text block we just added
                blocks.append({"type": "heading", "content": content, "level": 2})
                current_block = None
                i += 2  # Skip the underline
                continue

        # Handle images: ![alt](url)
        image_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)(?:\s*(.*))?$", stripped_line)
        if image_match and not in_quote and not in_list:
            if current_block:
                blocks.append(current_block)

            alt_text = image_match.group(1) or ""
            url = image_match.group(2)
            caption = image_match.group(3) or None

            img_block = {"type": "image", "content": "", "url": url, "alt": alt_text}
            if caption:
                img_block["caption"] = caption

            blocks.append(img_block)
            current_block = None
            i += 1
            continue

        # Handle block quotes
        if stripped_line.startswith(">") and not in_list:
            quote_line = stripped_line[1:].strip()

            # Check for attribution line
            attribution_match = re.match(r"^[\u2014-]\s+(.+)$", quote_line)

            if not in_quote:
                # Start of quote
                if current_block:
                    blocks.append(current_block)
                in_quote = True
                quote_lines = []
                quote_has_attribution = False

                if attribution_match:
                    quote_has_attribution = True
                    attribution = attribution_match.group(1)
                    # Don't add this to quote_lines as it's attribution
                else:
                    quote_lines.append(quote_line)
            else:
                # Continuing quote
                if attribution_match:
                    quote_has_attribution = True
                    attribution = attribution_match.group(1)
                    # Don't add this to quote_lines as it's attribution
                else:
                    quote_lines.append(quote_line)

            i += 1
            continue
        elif in_quote:
            # End of quote block
            quote_content = "\n".join(quote_lines).strip()
            quote_block = {"type": "quote", "content": quote_content}

            if quote_has_attribution:
                quote_block["attribution"] = attribution

            blocks.append(quote_block)
            in_quote = False
            current_block = None
            # Don't increment i, process this line again
            continue

        # Handle lists
        list_match = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", stripped_line)
        if list_match:
            indent = len(list_match.group(1))
            marker = list_match.group(2)
            item_content = list_match.group(3)
            is_ordered = bool(re.match(r"\d+\.", marker))

            if not in_list:
                # Start of a new list
                if current_block:
                    blocks.append(current_block)

                in_list = True
                current_list_indent = indent
                list_items = [item_content]
                list_type = "ordered" if is_ordered else "unordered"
            else:
                # Continuing a list
                # Check if this is a new list (different indent or type)
                if (indent != current_list_indent) or (is_ordered != (list_type == "ordered")):
                    # Different list - end current one and start new
                    blocks.append(
                        {
                            "type": "list",
                            "content": "",
                            "items": list_items,
                            "list_type": list_type,
                        }
                    )
                    list_items = [item_content]
                    current_list_indent = indent
                    list_type = "ordered" if is_ordered else "unordered"
                else:
                    # Same list - add item
                    list_items.append(item_content)

            i += 1
            continue
        elif in_list and stripped_line == "":
            # Empty line - check if next non-empty line continues the list
            next_i = i + 1
            while next_i < len(lines) and not lines[next_i].strip():
                next_i += 1

            if next_i < len(lines):
                next_line = lines[next_i]
                next_match = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", next_line)
                if next_match and len(next_match.group(1)) == current_list_indent:
                    # Next line continues this list after blank line(s)
                    i = next_i
                    continue

            # End of list
            blocks.append(
                {
                    "type": "list",
                    "content": "",
                    "items": list_items,
                    "list_type": list_type,
                }
            )
            in_list = False
            current_block = None
            i += 1
            continue
        elif in_list:
            # Not a list item - end list and process line again
            blocks.append(
                {
                    "type": "list",
                    "content": "",
                    "items": list_items,
                    "list_type": list_type,
                }
            )
            in_list = False
            # Don't increment i, process this line again
            continue

        # Handle normal text blocks with proper paragraph breaks (blank lines)
        if stripped_line or (current_block and current_block["type"] == "text"):
            if stripped_line == "" and current_block and current_block["type"] == "text":
                # Empty line after text - end paragraph
                blocks.append(current_block)
                current_block = None
            elif not current_block:
                # Start new text block
                current_block = {"type": "text", "content": stripped_line}
            else:
                # Continue existing text block
                # In Markdown, single line breaks don't create new paragraphs
                # Add a space unless the line was actually empty
                if current_block["content"] and stripped_line:
                    current_block["content"] += "\n" + stripped_line
                elif stripped_line:
                    current_block["content"] += stripped_line
                else:
                    # This is an empty line within a text block (preserve it)
                    current_block["content"] += "\n"

        i += 1

    # Handle unclosed blocks
    if current_block:
        blocks.append(current_block)

    if in_quote:
        quote_content = "\n".join(quote_lines).strip()
        quote_block = {"type": "quote", "content": quote_content}
        if quote_has_attribution:
            quote_block["attribution"] = attribution
        blocks.append(quote_block)

    if in_list:
        blocks.append({"type": "list", "content": "", "items": list_items, "list_type": list_type})

    if in_code_block:
        # Unclosed code block - best effort to add it
        blocks.append(current_block)

    return blocks


def convert_block_to_blockdoc(block: Dict[str, str]) -> Optional[Block]:
    """
    Convert a markdown block to a BlockDoc block

    Args:
        block (Dict[str, str]): Block data containing type and content

    Returns:
        Optional[Block]: A Block instance or None if conversion fails
    """
    block_type = block.get("type")

    # Generate a semantic ID based on content
    block_id = generate_block_id(block)

    try:
        if block_type == "text":
            content = block.get("content", "").strip()
            if not content:  # Skip empty text blocks
                return None
            return Block.text(block_id, content)

        elif block_type == "heading":
            level = block.get("level", 2)
            content = block.get("content", "").strip()
            return Block.heading(block_id, level, content)

        elif block_type == "code":
            language = block.get("language", "plain")
            content = block.get("content", "").strip()
            return Block.code(block_id, language, content)

        elif block_type == "image":
            url = block.get("url", "")
            alt = block.get("alt", "")
            caption = block.get("caption")
            return Block.image(block_id, url, alt, caption)

        elif block_type == "list":
            items = block.get("items", [])
            list_type = block.get("list_type", "unordered")
            return Block.list(block_id, items, list_type)

        elif block_type == "quote":
            content = block.get("content", "").strip()
            attribution = block.get("attribution")
            return Block.quote(block_id, content, attribution)

        elif block_type == "divider":
            return Block.divider(block_id)

        else:
            # Unknown block type, convert to text
            content = block.get("content", "").strip()
            return Block.text(block_id, content) if content else None
    except Exception as e:
        # If anything goes wrong, return None
        print(f"Error converting block to BlockDoc: {e}")
        return None


def generate_block_id(block: Dict[str, str]) -> str:
    """
    Generate a semantic ID for a block based on its content

    Args:
        block (Dict[str, str]): Block data

    Returns:
        str: A semantic ID for the block
    """
    block_type = block.get("type")
    content = block.get("content", "").strip()

    # For headings, create an ID from the content
    if block_type == "heading" and content:
        # Convert to lowercase, replace spaces with hyphens, remove non-alphanumeric
        slug = re.sub(r"[^\w\s-]", "", content.lower())
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        return slug[:40]  # Limit length of ID

    # For other block types, use the type as a prefix
    if block_type:
        prefix = block_type

        # For specific block types, enhance the ID
        if block_type == "code" and block.get("language"):
            prefix = f"code-{block.get('language')}"
        elif block_type == "list":
            prefix = f"{block.get('list_type', 'unordered')}-list"

        # Add a short random suffix to ensure uniqueness
        suffix = str(uuid.uuid4())[:8]
        return f"{prefix}-{suffix}"

    # Fallback to a generic ID
    return f"block-{str(uuid.uuid4())[:8]}"
