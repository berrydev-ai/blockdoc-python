"""
BlockDoc Markdown Conversion Example

This example demonstrates converting Markdown to BlockDoc format
"""

import os
import sys
from datetime import datetime

# Add the parent directory to sys.path to import blockdoc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blockdoc import markdown_to_blockdoc

# Sample markdown content
SAMPLE_MARKDOWN = """# Markdown to BlockDoc Conversion

This is a demonstration of converting **Markdown** content to BlockDoc format.

## Key Features

BlockDoc makes it easy to work with structured content:

- Maintains semantic structure
- Preserves formatting
- Creates meaningful block IDs

### Code Examples

Here's an example of Python code:

```python
from blockdoc import markdown_to_blockdoc

# Convert markdown to BlockDoc
doc = markdown_to_blockdoc(markdown_text)

# Export as JSON
json_str = doc.to_json()
print(json_str)
```

## Images and Media

Images are properly converted:

![Example image](https://placehold.co/600x400?text=Example+Image) Example image caption

## Block Quotes

BlockDoc handles various content types:

> This is a block quote that will be properly converted
> to a BlockDoc quote block, preserving its formatting
> and presentation.
> — Attribution Source

---

## Lists

1. Ordered lists work great
2. With multiple items
3. Preserving the numbering

* Unordered lists too
* With proper nesting
* And formatting

## The End

This example shows how Markdown can be seamlessly converted to BlockDoc format, preserving
the document structure while enabling all the benefits of block-based content.
"""


def main():
    """
    Main function to run the example
    """
    print("Converting Markdown to BlockDoc format...")
    doc = markdown_to_blockdoc(
        SAMPLE_MARKDOWN,
        metadata={
            "author": "BlockDoc Team",
            "publishedDate": datetime.now().isoformat(),
            "tags": ["markdown", "conversion", "example"],
        },
    )

    # Validate the document against the schema
    print("Validating against schema...")
    try:
        doc.validate()
        print("✓ Document is valid")
    except ValueError as e:
        print(f"✗ Validation failed: {e}")
        return

    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save the document as JSON
    print("Saving document as JSON...")
    with open(os.path.join(output_dir, "markdown-converted.json"), "w", encoding="utf-8") as f:
        f.write(doc.to_json(indent=2))

    # Render back to Markdown
    print("Rendering back to Markdown...")
    markdown = doc.render_to_markdown()
    with open(os.path.join(output_dir, "markdown-roundtrip.md"), "w", encoding="utf-8") as f:
        f.write(markdown)

    # Render to HTML
    print("Rendering to HTML...")
    html = doc.render_to_html()
    with open(os.path.join(output_dir, "markdown-converted.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # Display block structure
    print("\nDocument structure:")
    for i, block in enumerate(doc.article["blocks"]):
        print(f"{i + 1}. Type: {block['type']}, ID: {block['id']}")

    print("\nExample complete! Output files saved to:", output_dir)
    print("• markdown-converted.json - The BlockDoc document in JSON format")
    print("• markdown-roundtrip.md - The document rendered back to Markdown")
    print("• markdown-converted.html - The document rendered to HTML")


if __name__ == "__main__":
    main()
