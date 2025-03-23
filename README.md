# BlockDoc

A simple, powerful standard for structured content that works beautifully with LLMs, humans, and modern editors.

[![PyPI version](https://img.shields.io/pypi/v/blockdoc.svg)](https://pypi.org/project/blockdoc/)
[![Python versions](https://img.shields.io/pypi/pyversions/blockdoc.svg)](https://pypi.org/project/blockdoc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Why BlockDoc?

BlockDoc provides a lightweight, flexible format for structured content that is:

- **LLM-friendly**: Optimized for AI generation and targeted modifications
- **Simple**: Flat structure with semantic IDs and minimal nesting
- **Extensible**: Core block types with room for custom extensions
- **Framework-agnostic**: Works with any frontend or backend technology
- **Database-ready**: Easy to store and query in SQL or NoSQL databases

## Core Concepts

BlockDoc is based on a block-based architecture where content is organized into discrete, individually addressable blocks. Each block has:

- A semantic ID (like 'intro', 'section-1')
- A block type ('text', 'heading', 'image', 'code')
- Content (in Markdown for text-based blocks)
- Optional metadata

This architecture enables:

- Targeted updates to specific sections
- Better organization of content
- Easy integration with LLMs
- Flexible rendering in different formats

### Core Block Types

1. **Text** - Standard paragraphs with Markdown support
2. **Heading** - Section headers with configurable levels
3. **Image** - Pictures with src, alt text, and optional caption
4. **Code** - Code blocks with syntax highlighting
5. **List** - Ordered or unordered lists
6. **Quote** - Blockquote content
7. **Embed** - Embedded content (videos, social media posts)
8. **Divider** - Horizontal rule/separator

### Design Principles

1. **Simplicity**: Minimal structure with only necessary properties
2. **LLM-Friendly**: Optimized for AI content generation and modification
3. **Human-Editable**: Clear, readable format for direct editing
4. **Database-Ready**: Easily stored in SQL or NoSQL databases
5. **Extensible**: Core types with support for custom block types
6. **Semantic**: Meaningful IDs for blocks rather than auto-generated IDs
7. **Portable**: Framework-agnostic with multiple render targets

```json
{
  "article": {
    "title": "Getting Started with BlockDoc",
    "blocks": [
      {
        "id": "intro",
        "type": "text",
        "content": "BlockDoc makes structured content **simple**."
      },
      {
        "id": "first-steps",
        "type": "heading",
        "level": 2,
        "content": "First Steps"
      },
      {
        "id": "step-one",
        "type": "text",
        "content": "Install BlockDoc using pip: `pip install blockdoc`"
      }
    ]
  }
}
```

## Installation

Install BlockDoc from PyPI:

```bash
pip install blockdoc
```

## Usage

```python
from blockdoc import BlockDocDocument, Block

# Create a new document
doc = BlockDocDocument({
    "title": "My First BlockDoc Post",
})

# Add blocks using factory methods
doc.add_block(Block.text("intro", "Welcome to my first post!"))
doc.add_block(Block.heading("section-1", 2, "Getting Started"))
doc.add_block(Block.text("content-1", "This is **formatted** content with [links](https://example.com)."))

# Render to HTML
html = doc.render_to_html()
print(html)

# Render to Markdown
markdown = doc.render_to_markdown()
print(markdown)

# Export to JSON
json_str = doc.to_json()
print(json_str)
```

### Working with LLMs

BlockDoc shines when generating or modifying content with LLMs:

```python
from blockdoc import BlockDocDocument
import openai

# Update a specific section using an LLM
async def update_section(document, block_id, prompt):
    block = document.get_block(block_id)
    
    response = await openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"Update the following content to {prompt}. Return only the updated content."
            },
            {
                "role": "user",
                "content": block["content"],
            },
        ],
    )
    
    document.update_block(block_id, {
        "content": response.choices[0].message.content,
    })
    
    return document
```

## Documentation

### Specification

- [Full Specification](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/spec/blockdoc-specification.md)

### API Reference

- [Block Class](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/api-docs/block.md)
- [BlockDocDocument Class](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/api-docs/document.md)
- [HTML Renderer](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/api-docs/renderers/html.md)
- [Markdown Renderer](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/api-docs/renderers/markdown.md)
- [Sanitization Utilities](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/api-docs/utils/sanitize.md)

### Tutorials

- [Getting Started](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/tutorials/getting-started.md)
- [Block Types](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/tutorials/block-types.md)
- [LLM Integration](https://github.com/berrydev-ai/blockdoc-python/blob/main/docs/tutorials/llm-integration.md)

### Examples

- [Simple Blog Generator](https://github.com/berrydev-ai/blockdoc-python/blob/main/examples/simple-blog/)
- [LLM Content Integration](https://github.com/berrydev-ai/blockdoc-python/blob/main/examples/llm-integration/)
- [Basic Usage Example](https://github.com/berrydev-ai/blockdoc-python/blob/main/examples/basic_example.py)

## Development

### Installation

```bash
# Clone the repository
git clone https://github.com/berrydev-ai/blockdoc-python.git
cd blockdoc-python

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Testing

BlockDoc uses pytest for testing. To run the tests:

```bash
# Run tests
pytest

# Run tests with coverage report
pytest --cov=blockdoc

# Run a specific test file
pytest tests/core/test_block.py

# Run linting and formatting with ruff
ruff check .
ruff format .
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](https://github.com/berrydev-ai/blockdoc-python/blob/main/CONTRIBUTING.md) for details on how to contribute, including our testing guidelines.

## License

[MIT](https://github.com/berrydev-ai/blockdoc-python/blob/main/LICENSE)