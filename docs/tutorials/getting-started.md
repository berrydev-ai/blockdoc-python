# Getting Started with BlockDoc

This tutorial will guide you through the basics of using BlockDoc to create, manipulate, and render structured content.

## Installation

Install BlockDoc from PyPI:

```bash
pip install blockdoc
```

## Creating Your First Document

Let's create a simple blog post using BlockDoc:

```python
from blockdoc import BlockDocDocument, Block

# Create a new document with a title and metadata
blog_post = BlockDocDocument({
    "title": "My First BlockDoc Post",
    "metadata": {
        "author": "Your Name",
        "publishedDate": "2025-03-23T10:00:00Z",
        "tags": ["blockdoc", "tutorial", "beginner"]
    }
})

# Add an introduction
blog_post.add_block(Block.text(
    "intro",
    "Welcome to my **first post** using BlockDoc! In this post, I'll explain why BlockDoc is a great choice for structured content."
))

# Add a heading
blog_post.add_block(Block.heading(
    "benefits",  # Semantic ID describing the section's purpose
    2,           # Heading level (h2)
    "Benefits of BlockDoc"
))

# Add a list of benefits
blog_post.add_block(Block.list(
    "benefits-list",
    [
        "**LLM-friendly**: Designed for AI generation and targeted updates",
        "**Simple structure**: Easy to understand and work with",
        "**Semantic IDs**: Blocks have meaningful identifiers",
        "**Flexible rendering**: Output to HTML, Markdown, or custom formats"
    ],
    "unordered"  # List type (unordered or ordered)
))

# Add a code example
blog_post.add_block(Block.code(
    "code-example",
    "python",    # Language for syntax highlighting
    """from blockdoc import BlockDocDocument, Block

doc = BlockDocDocument({
    "title": "Example Document"
})

doc.add_block(Block.text("intro", "This is an introduction."))"""
))

# Add a conclusion
blog_post.add_block(Block.text(
    "conclusion",
    "As you can see, BlockDoc makes it easy to create structured content that's both human and machine-friendly."
))
```

## Validating Your Document

BlockDoc includes schema validation to ensure documents follow the correct structure:

```python
try:
    blog_post.validate()
    print("Document is valid!")
except ValueError as e:
    print(f"Validation error: {str(e)}")
```

## Rendering to Different Formats

One of BlockDoc's strengths is the ability to render content in different formats:

### Rendering to HTML

```python
# Get the HTML representation
html = blog_post.render_to_html()

# Save to a file
with open("blog_post.html", "w", encoding="utf-8") as f:
    f.write(html)
```

### Rendering to Markdown

```python
# Get the Markdown representation
markdown = blog_post.render_to_markdown()

# Save to a file
with open("blog_post.md", "w", encoding="utf-8") as f:
    f.write(markdown)
```

### Exporting to JSON

```python
# Get the JSON representation
json_str = blog_post.to_json(indent=2)

# Save to a file
with open("blog_post.json", "w", encoding="utf-8") as f:
    f.write(json_str)
```

## Working with Existing Documents

You can also load and modify existing BlockDoc documents:

### Loading from JSON

```python
with open("blog_post.json", "r", encoding="utf-8") as f:
    json_str = f.read()

# Create a document from JSON
loaded_doc = BlockDocDocument.from_json(json_str)
```

### Updating Blocks

```python
# Update a specific block by ID
loaded_doc.update_block("intro", {
    "content": "Welcome to my **updated** introduction using BlockDoc!"
})

# Render the updated document
updated_html = loaded_doc.render_to_html()
```

### Moving and Removing Blocks

```python
# Move a block to a different position
loaded_doc.move_block("conclusion", 1)  # Move conclusion to the second position

# Remove a block
loaded_doc.remove_block("code-example")
```

## Adding Different Block Types

BlockDoc supports multiple block types for different content needs:

### Image Block

```python
blog_post.add_block(Block.image(
    "screenshot",
    "https://example.com/blockdoc-screenshot.jpg",
    "Screenshot of BlockDoc in action",
    "Figure 1: BlockDoc document structure"  # Optional caption
))
```

### Quote Block

```python
blog_post.add_block(Block.quote(
    "testimonial",
    "BlockDoc has revolutionized how we structure content for our LLM applications.",
    "Jane Developer, AI Solutions Inc."  # Optional attribution
))
```

### Embed Block

```python
blog_post.add_block(Block.embed(
    "tutorial-video",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "youtube",  # Embed type
    "Video tutorial on using BlockDoc"  # Optional caption
))
```

### Divider Block

```python
blog_post.add_block(Block.divider("section-divider"))
```

## Best Practices

1. **Use Semantic IDs**: Choose IDs that describe the content purpose, not just sequential numbers
2. **Organize Content in Logical Blocks**: Keep blocks focused on discrete units of content
3. **Validate Documents**: Always validate before rendering or storage
4. **Handle Errors Gracefully**: Implement proper error handling for validation and operations
5. **Sanitize External Content**: Use sanitization utilities for user-provided content

## Next Steps

Now that you've learned the basics of using BlockDoc, check out these resources to deepen your knowledge:

- [Block Types Tutorial](block-types.md) - Explore all the available block types
- [LLM Integration Tutorial](llm-integration.md) - Learn how to use BlockDoc with language models
- [API Reference](../api-docs/) - Complete reference documentation
- [Examples](../../examples/) - Real-world examples of BlockDoc in action