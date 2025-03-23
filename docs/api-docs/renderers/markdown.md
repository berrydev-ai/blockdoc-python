# Markdown Renderer API Reference

The Markdown renderer converts BlockDoc documents to Markdown.

## Import

```python
from blockdoc.renderers.markdown import render_to_markdown
```

## Functions

### `render_to_markdown(article)`

Renders a BlockDoc document to Markdown.

**Parameters:**

- `article` (dict): The article object from a BlockDoc document

**Returns:**

- `str`: Markdown representation

**Raises:**

- `ValueError`: If the article structure is invalid

**Example:**

```python
from blockdoc import BlockDocDocument
from blockdoc.renderers.markdown import render_to_markdown

doc = BlockDocDocument({
    "title": "My Document",
})
doc.add_block({"id": "intro", "type": "text", "content": "Introduction"})

# Method 1: Use the document's render method
markdown = doc.render_to_markdown()

# Method 2: Use the renderer directly
markdown = render_to_markdown(doc.article)
```

## Block Rendering Functions

The Markdown renderer includes specialized functions for rendering each block type. These are typically used internally by the main `render_to_markdown` function, but can be used directly if needed.

### `render_block_to_markdown(block)`

Renders a single block to Markdown.

**Parameters:**

- `block` (dict): Block data

**Returns:**

- `str`: Markdown representation of the block

### Block Type-Specific Renderers

Each block type has its own rendering function:

- `render_text_block_to_markdown(block)`: Renders text blocks (passes through Markdown content)
- `render_heading_block_to_markdown(block)`: Renders heading blocks with appropriate number of # symbols
- `render_image_block_to_markdown(block)`: Renders image blocks with Markdown image syntax
- `render_code_block_to_markdown(block)`: Renders code blocks with Markdown code fence syntax
- `render_list_block_to_markdown(block)`: Renders list blocks with proper formatting
- `render_quote_block_to_markdown(block)`: Renders quote blocks with > prefix
- `render_embed_block_to_markdown(block)`: Renders embed blocks as links
- `render_divider_block_to_markdown()`: Renders divider blocks as horizontal rules (---)

## Markdown Output Structure

The Markdown renderer produces clean, structured Markdown with the following elements:

- Document title: `# Title`
- Blocks separated by newlines
- Special formatting for each block type
- Block IDs preserved as HTML comments <!-- block-id: id --> for reference

### Example Output

```markdown
# My Document

<!-- block-id: intro -->
This is the **introduction** paragraph with a [link](https://example.com).

<!-- block-id: section-1 -->
## Section Title

<!-- block-id: feature-list -->
- First item
- Second item
- Third item

<!-- block-id: code-example -->
```python
def hello_world():
    print("Hello, World!")
```

<!-- block-id: quote -->
> This is a quote
> 
> — Source

<!-- block-id: divider -->
---
```

## Usage Considerations

### Preserving Block Identity

The Markdown renderer adds HTML comments containing block IDs to make it easier to map Markdown content back to the original BlockDoc structure. This can be useful for round-trip editing workflows.

### Limitations

Some BlockDoc features don't have direct Markdown equivalents:

1. **Embeds**: Rendered as links since Markdown doesn't natively support embeds
2. **Complex Images**: Caption information is included as text under the image
3. **Metadata**: Document metadata is not included in the Markdown output

### Custom Rendering

You can extend the Markdown renderer with custom functions for specific block types:

```python
from blockdoc.renderers.markdown import render_to_markdown

def custom_render_to_markdown(article):
    # Custom pre-processing if needed
    markdown = render_to_markdown(article)
    # Custom post-processing if needed
    return markdown
```

## Complete Example

```python
from blockdoc import BlockDocDocument, Block

# Create a document
doc = BlockDocDocument({
    "title": "BlockDoc Example",
})

# Add various block types
doc.add_block(Block.text("intro", "This is an introduction to **BlockDoc**."))
doc.add_block(Block.heading("section-1", 2, "Section One"))
doc.add_block(Block.text("para-1", "This is a paragraph with [a link](https://example.com)."))
doc.add_block(Block.code("code-1", "python", "print('Hello, BlockDoc!')"))
doc.add_block(Block.list("list-1", ["Item 1", "Item 2", "Item 3"], "unordered"))
doc.add_block(Block.quote("quote-1", "This is a quote", "Author"))
doc.add_block(Block.divider("div-1"))

# Render to Markdown
markdown = doc.render_to_markdown()
print(markdown)
```