"""
Test the Markdown to BlockDoc converter
"""

from blockdoc.conversions.markdown import markdown_to_blockdoc
from blockdoc.core.document import BlockDocDocument


def test_markdown_to_blockdoc_basic():
    """Test basic markdown conversion"""
    markdown = """# Test Document
    
This is a paragraph with **bold** and *italic* text.
    """

    doc = markdown_to_blockdoc(markdown)

    assert isinstance(doc, BlockDocDocument)
    assert doc.article["title"] == "Test Document"
    assert len(doc.article["blocks"]) == 1
    assert doc.article["blocks"][0]["type"] == "text"
    assert "bold" in doc.article["blocks"][0]["content"]


def test_markdown_to_blockdoc_with_explicit_title():
    """Test markdown conversion with explicit title"""
    markdown = """# Test Document
    
This is a paragraph.
    """

    doc = markdown_to_blockdoc(markdown, title="Explicit Title")

    assert doc.article["title"] == "Explicit Title"


def test_markdown_to_blockdoc_with_metadata():
    """Test markdown conversion with metadata"""
    markdown = """# Test Document
    
This is a paragraph.
    """

    metadata = {"author": "Test Author", "tags": ["test", "markdown"]}

    doc = markdown_to_blockdoc(markdown, metadata=metadata)

    assert doc.article["metadata"]["author"] == "Test Author"
    assert "test" in doc.article["metadata"]["tags"]


def test_markdown_to_blockdoc_blocks():
    """Test conversion of different markdown block types"""
    markdown = """# Heading 1

## Heading 2

This is a paragraph.

- List item 1
- List item 2

1. Ordered item 1
2. Ordered item 2

```python
def test():
    pass
```

> This is a quote
> Multiple lines
> — Attribution

![Alt text](https://example.com/image.jpg) Caption

---

Final paragraph.
"""

    doc = markdown_to_blockdoc(markdown)

    # Check number of blocks (should have 9 blocks)
    assert len(doc.article["blocks"]) == 9

    # Extract block types
    block_types = [block["type"] for block in doc.article["blocks"]]

    # Check that we have all the expected block types
    assert "heading" in block_types
    assert "text" in block_types
    assert "list" in block_types
    assert "code" in block_types
    assert "quote" in block_types
    assert "image" in block_types
    assert "divider" in block_types

    # Check heading levels
    headings = [block for block in doc.article["blocks"] if block["type"] == "heading"]
    assert any(h["level"] == 2 for h in headings)

    # Check list types
    lists = [block for block in doc.article["blocks"] if block["type"] == "list"]
    list_types = [l["list_type"] for l in lists]
    assert "ordered" in list_types
    assert "unordered" in list_types

    # Check code block language
    code_blocks = [block for block in doc.article["blocks"] if block["type"] == "code"]
    assert code_blocks[0]["language"] == "python"

    # Check quote attribution
    quotes = [block for block in doc.article["blocks"] if block["type"] == "quote"]
    assert "Attribution" in quotes[0]["attribution"]


def test_empty_markdown():
    """Test conversion of empty markdown"""
    doc = markdown_to_blockdoc("")

    assert doc.article["title"] == "Untitled Document"
    assert len(doc.article["blocks"]) == 0
