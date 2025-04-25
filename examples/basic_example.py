"""
BlockDoc Basic Example

This example demonstrates creating and rendering a simple document using BlockDoc
"""

import os
import subprocess
import sys
from datetime import datetime

# Add the parent directory to sys.path to import blockdoc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Check and install required dependencies
try:
    import jsonschema
    import markdown
    import pygments
except ImportError:
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "pygments", "jsonschema"])
    print("Dependencies installed successfully.")

from blockdoc import Block, BlockDocDocument


def create_blog_post():
    """
    Create a sample blog post

    Returns:
        BlockDocDocument: The created document
    """
    # Create a new document
    blog_post = BlockDocDocument(
        {
            "title": "Getting Started with BlockDoc",
            "metadata": {
                "author": "BlockDoc Team",
                "publishedDate": datetime.now().isoformat(),
                "tags": ["blockdoc", "tutorial", "content", "structured-data"],
            },
        }
    )

    # Add an introduction
    blog_post.add_block(
        Block.text(
            "intro",
            "Welcome to **BlockDoc**, a simple yet powerful format for structured content. "
            "In this tutorial, we'll explore the basics of creating and working with BlockDoc documents.",
        )
    )

    # Add a heading
    blog_post.add_block(Block.heading("what-is-blockdoc", 2, "What is BlockDoc?"))

    # Add content explaining BlockDoc
    blog_post.add_block(
        Block.text(
            "blockdoc-explanation",
            "BlockDoc is a structured content format designed for:\n\n"
            "* **LLM-friendly** - Optimized for generation and modification by AI\n"
            "* **Block-based** - Content is divided into modular blocks with semantic IDs\n"
            "* **Flexible** - Supports various content types and nested structures\n"
            "* **Database-ready** - Easy to store in document databases\n"
            "* **Renderer-agnostic** - Output to HTML, Markdown, or other formats",
        )
    )

    # Add a code example
    blog_post.add_block(
        Block.code(
            "code-example",
            "python",
            """# Create a new BlockDoc document
doc = BlockDocDocument({
    "title": "My First Document",
})

# Add some content blocks
doc.add_block(Block.heading("intro-heading", 2, "Introduction"))
doc.add_block(Block.text("intro-text", "This is my **first** BlockDoc document."))

# Render to HTML
html = doc.render_to_html()
print(html)""",
        )
    )

    # Add an image
    blog_post.add_block(
        Block.image(
            "sample-image",
            "https://placehold.co/600x400?text=BlockDoc+Example",
            "A sample BlockDoc document structure",
            "Figure 1: Visual representation of a BlockDoc document",
        )
    )

    # Add another heading
    blog_post.add_block(Block.heading("block-types", 2, "Supported Block Types"))

    # Add a list of block types
    blog_post.add_block(
        Block.list(
            "block-types-list",
            [
                "**Text**: Markdown-formatted text content",
                "**Heading**: Section headings with levels 1-6",
                "**Image**: Images with URL, alt text, and optional caption",
                "**Code**: Code snippets with language highlighting",
                "**List**: Ordered or unordered lists",
                "**Quote**: Blockquotes with optional attribution",
                "**Embed**: Embedded content like videos or tweets",
                "**Divider**: Horizontal dividers between sections",
            ],
            "unordered",
        )
    )

    # Add a quote
    blog_post.add_block(Block.text("quote-intro", "BlockDoc was designed with a specific philosophy in mind:"))

    quote_block = Block(
        {
            "id": "philosophy-quote",
            "type": "quote",
            "content": "Content should be structured in a way that is meaningful to both humans and machines, allowing for precise updates and transformations while maintaining semantic context.",
            "attribution": "BlockDoc Design Principles",
        }
    )

    blog_post.add_block(quote_block)

    # Add a conclusion
    blog_post.add_block(Block.heading("conclusion", 2, "Getting Started"))

    blog_post.add_block(
        Block.text(
            "conclusion-text",
            "Ready to try BlockDoc for yourself? Check out our [GitHub repository](https://github.com/berrydev-ai/blockdoc-python) and follow the installation instructions to get started.\n\n"
            "BlockDoc is perfect for content-heavy applications, CMS systems, documentation sites, and anywhere else you need structured, maintainable content.",
        )
    )

    # Add a divider
    blog_post.add_block(Block.divider("end-divider"))

    # Return the document
    return blog_post


def main():
    """
    Main function to run the example
    """
    print("Creating a sample BlockDoc blog post...")
    blog_post = create_blog_post()

    # Validate the document against the schema
    print("Validating against schema...")
    try:
        blog_post.validate()
        print("✓ Document is valid")
    except ValueError as e:
        print(f"✗ Validation failed: {e}")
        return

    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save the document as JSON
    print("Saving document as JSON...")
    with open(os.path.join(output_dir, "blog-post.json"), "w", encoding="utf-8") as f:
        f.write(blog_post.to_json())

    # Render to HTML
    print("Rendering to HTML...")
    html = blog_post.render_to_html()
    with open(os.path.join(output_dir, "blog-post.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # Render to Markdown
    print("Rendering to Markdown...")
    markdown = blog_post.render_to_markdown()
    with open(os.path.join(output_dir, "blog-post.md"), "w", encoding="utf-8") as f:
        f.write(markdown)

    # Example of updating a block
    print("Updating a block...")
    blog_post.update_block(
        "blockdoc-explanation",
        {
            "content": "BlockDoc is a powerful structured content format designed for:\n\n"
            "* **LLM-friendly** - Optimized for generation and modification by AI\n"
            "* **Block-based** - Content is divided into modular blocks with semantic IDs\n"
            "* **Flexible** - Supports various content types and nested structures\n"
            "* **Database-ready** - Easy to store in document databases\n"
            "* **Renderer-agnostic** - Output to HTML, Markdown, or other formats\n"
            "* **Version control friendly** - Easy to track changes to specific content blocks"
        },
    )

    print("Saving updated document...")
    with open(os.path.join(output_dir, "blog-post-updated.json"), "w", encoding="utf-8") as f:
        f.write(blog_post.to_json())

    print("Example complete! Output files saved to:", output_dir)
    print("• blog-post.json - The BlockDoc document in JSON format")
    print("• blog-post.html - The document rendered to HTML")
    print("• blog-post.md - The document rendered to Markdown")
    print("• blog-post-updated.json - The document after updating a block")


if __name__ == "__main__":
    main()
