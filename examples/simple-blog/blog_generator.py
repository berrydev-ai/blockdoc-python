"""
BlockDoc Simple Blog Generator

This example demonstrates using BlockDoc to create and manage blog posts.
"""

import argparse
import datetime
import json
import os
import sys

# Add the parent directory to sys.path to import blockdoc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from blockdoc import Block, BlockDocDocument


def create_blog_post(title, author, content_json=None):
    """
    Create a blog post using BlockDoc

    Args:
        title (str): Blog post title
        author (str): Blog post author
        content_json (str): Optional path to JSON file with content structure

    Returns:
        BlockDocDocument: The created blog post
    """
    # Create a new document with metadata
    blog_post = BlockDocDocument(
        {
            "title": title,
            "metadata": {
                "author": author,
                "publishedDate": datetime.datetime.now().isoformat(),
                "type": "blog-post",
                "tags": ["blockdoc", "example", "blog"],
            },
        }
    )

    if content_json:
        # Load content structure from JSON file
        with open(content_json, encoding="utf-8") as f:
            content_structure = json.load(f)

        # Process the content structure
        for item in content_structure:
            block_type = item.get("type")
            block_id = item.get("id")

            if block_type == "text":
                blog_post.add_block(Block.text(block_id, item.get("content", "")))

            elif block_type == "heading":
                blog_post.add_block(Block.heading(block_id, item.get("level", 2), item.get("content", "")))

            elif block_type == "image":
                blog_post.add_block(
                    Block.image(
                        block_id,
                        item.get("url", ""),
                        item.get("alt", ""),
                        item.get("caption"),
                    )
                )

            elif block_type == "code":
                blog_post.add_block(Block.code(block_id, item.get("language", "text"), item.get("content", "")))

            elif block_type == "list":
                blog_post.add_block(
                    Block.list(
                        block_id,
                        item.get("items", []),
                        item.get("list_type", "unordered"),
                    )
                )

            elif block_type == "quote":
                blog_post.add_block(Block.quote(block_id, item.get("content", ""), item.get("attribution")))

            elif block_type == "divider":
                blog_post.add_block(Block.divider(block_id))

    else:
        # Create a default structure if no JSON provided
        blog_post.add_block(
            Block.text(
                "introduction",
                "Welcome to this blog post created with BlockDoc! BlockDoc makes it easy to create structured content that can be rendered in different formats.",
            )
        )

        blog_post.add_block(Block.heading("about-blockdoc", 2, "About BlockDoc"))

        blog_post.add_block(
            Block.text(
                "blockdoc-description",
                "BlockDoc is a simple, powerful standard for structured content that works beautifully with LLMs, humans, and modern editors. It provides a block-based architecture where content is organized into discrete, individually addressable blocks.",
            )
        )

        blog_post.add_block(Block.heading("features-heading", 2, "Key Features"))

        blog_post.add_block(
            Block.list(
                "features-list",
                [
                    "**LLM-friendly**: Optimized for AI generation and modification",
                    "**Block-based**: Content is divided into semantic blocks",
                    "**Flexible**: Supports various content types and structures",
                    "**Renderer-agnostic**: Output to HTML, Markdown, or custom formats",
                ],
                "unordered",
            )
        )

        blog_post.add_block(
            Block.image(
                "example-image",
                "https://placehold.co/600x400?text=BlockDoc+Example",
                "Example BlockDoc structure visualization",
                "Figure: Visualization of a BlockDoc document structure",
            )
        )

        blog_post.add_block(Block.heading("code-example-heading", 2, "Code Example"))

        blog_post.add_block(
            Block.code(
                "python-example",
                "python",
                """from blockdoc import BlockDocDocument, Block

# Create a document
doc = BlockDocDocument({
    "title": "My Document"
})

# Add a text block
doc.add_block(Block.text("intro", "This is the introduction."))

# Render to HTML
html = doc.render_to_html()
""",
            )
        )

        blog_post.add_block(Block.heading("conclusion-heading", 2, "Conclusion"))

        blog_post.add_block(
            Block.text(
                "conclusion",
                "This example demonstrates how easy it is to create structured content with BlockDoc. Check out the [GitHub repository](https://github.com/berrydev-ai/blockdoc-python) for more information and examples.",
            )
        )

    return blog_post


def main():
    """
    Main function to run the blog generator
    """
    parser = argparse.ArgumentParser(description="Generate a blog post using BlockDoc")
    parser.add_argument("--title", default="BlockDoc Blog Example", help="Blog post title")
    parser.add_argument("--author", default="BlockDoc Team", help="Blog post author")
    parser.add_argument("--content", help="Path to JSON file with content structure")
    parser.add_argument("--output-dir", default="./output", help="Output directory for generated files")

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Create the blog post
    print(f"Creating blog post: {args.title} by {args.author}")
    blog_post = create_blog_post(args.title, args.author, args.content)

    # Validate the document
    print("Validating document...")
    try:
        blog_post.validate()
        print("✓ Document is valid")
    except ValueError as e:
        print(f"✗ Validation error: {e}")
        return

    # Create a slug from the title for filenames
    slug = args.title.lower().replace(" ", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")

    # Save as JSON
    json_path = os.path.join(args.output_dir, f"{slug}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(blog_post.to_json(indent=2))
    print(f"✓ Saved JSON to {json_path}")

    # Render to HTML
    html_path = os.path.join(args.output_dir, f"{slug}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        # Add basic styling
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .blockdoc-title {{ margin-bottom: 1.5rem; }}
        .blockdoc-block {{ margin-bottom: 1.5rem; }}
        .blockdoc-image {{ max-width: 100%; height: auto; }}
        .blockdoc-caption {{ font-size: 0.9rem; color: #666; text-align: center; margin-top: 0.5rem; }}
        .blockdoc-pre {{ background-color: #f5f5f5; border-radius: 4px; padding: 1rem; overflow-x: auto; }}
        .blockdoc-code {{ font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 0.9rem; }}
        .blockdoc-quote {{ border-left: 4px solid #ccc; padding-left: 1rem; font-style: italic; margin: 0; }}
        .blockdoc-attribution {{ display: block; text-align: right; font-style: normal; font-size: 0.9rem; margin-top: 0.5rem; }}
        .blockdoc-divider {{ border: 0; border-top: 1px solid #eee; margin: 2rem 0; }}
        .author-info {{ color: #666; font-size: 0.9rem; margin-bottom: 2rem; }}
        .blockdoc-list {{ padding-left: 20px; }}
    </style>
</head>
<body>
""".format(title=blog_post.article["title"])

        # Add author info
        html += f"""<div class="author-info">
    By {blog_post.article["metadata"].get("author", "Unknown")} | 
    Published: {blog_post.article["metadata"].get("publishedDate", "").split("T")[0]}
</div>
"""

        # Add the rendered content
        html += blog_post.render_to_html()

        # Close the HTML
        html += """
</body>
</html>
"""
        f.write(html)
    print(f"✓ Saved HTML to {html_path}")

    # Render to Markdown
    md_path = os.path.join(args.output_dir, f"{slug}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        # Add YAML frontmatter
        frontmatter = f"""---
title: "{blog_post.article["title"]}"
author: "{blog_post.article["metadata"].get("author", "Unknown")}"
date: "{blog_post.article["metadata"].get("publishedDate", "").split("T")[0]}"
tags: {blog_post.article["metadata"].get("tags", [])}
---

"""
        f.write(frontmatter + blog_post.render_to_markdown())
    print(f"✓ Saved Markdown to {md_path}")

    print("\nBlog post generation complete!")
    print(f"Files saved to {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    main()
