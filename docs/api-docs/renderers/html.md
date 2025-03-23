# HTML Renderer API Reference

The HTML renderer converts BlockDoc documents to HTML.

## Import

```python
from blockdoc.renderers.html import render_to_html
```

## Functions

### `render_to_html(article)`

Renders a BlockDoc document to HTML.

**Parameters:**

- `article` (dict): The article object from a BlockDoc document

**Returns:**

- `str`: HTML representation

**Raises:**

- `ValueError`: If the article structure is invalid

**Example:**

```python
from blockdoc import BlockDocDocument
from blockdoc.renderers.html import render_to_html

doc = BlockDocDocument({
    "title": "My Document",
})
doc.add_block({"id": "intro", "type": "text", "content": "Introduction"})

# Method 1: Use the document's render method
html = doc.render_to_html()

# Method 2: Use the renderer directly
html = render_to_html(doc.article)
```

## Block Rendering Functions

The HTML renderer includes specialized functions for rendering each block type. These are typically used internally by the main `render_to_html` function, but can be used directly if needed.

### `render_block(block)`

Renders a single block to HTML.

**Parameters:**

- `block` (dict): Block data

**Returns:**

- `str`: HTML representation of the block

### Block Type-Specific Renderers

Each block type has its own rendering function:

- `render_text_block(block)`: Renders text blocks using the markdown library
- `render_heading_block(block)`: Renders heading blocks with the appropriate h1-h6 tag
- `render_image_block(block)`: Renders image blocks with proper alt text and optional captions
- `render_code_block(block)`: Renders code blocks with syntax highlighting via Pygments
- `render_list_block(block)`: Renders list blocks as ordered or unordered lists
- `render_quote_block(block)`: Renders quote blocks as blockquotes with optional attribution
- `render_embed_block(block)`: Renders embed blocks for YouTube, Twitter, or generic embeds
- `render_divider_block()`: Renders divider blocks as horizontal rules

## HTML Output Structure

The HTML renderer produces semantic, structured HTML with appropriate classes for styling:

- Document wrapper: `<article class="blockdoc-article">`
- Document title: `<h1 class="blockdoc-title">`
- Block wrapper: `<div class="blockdoc-block blockdoc-{type}" data-block-id="{id}" data-block-type="{type}">`

### Example Output

```html
<article class="blockdoc-article">
  <h1 class="blockdoc-title">My Document</h1>
  
  <div class="blockdoc-block blockdoc-text" data-block-id="intro" data-block-type="text">
    <p>This is the <strong>introduction</strong> paragraph with a <a href="https://example.com">link</a>.</p>
  </div>
  
  <div class="blockdoc-block blockdoc-heading" data-block-id="section-1" data-block-type="heading">
    <h2>Section Title</h2>
  </div>
  
  <div class="blockdoc-block blockdoc-list" data-block-id="feature-list" data-block-type="list">
    <ul class="blockdoc-list blockdoc-list-unordered">
      <li>First item</li>
      <li>Second item</li>
      <li>Third item</li>
    </ul>
  </div>
</article>
```

## CSS Styling

The HTML renderer adds CSS classes to facilitate styling but does not include the CSS itself. Here's a sample CSS starter for styling BlockDoc documents:

```css
.blockdoc-article {
  max-width: 800px;
  margin: 0 auto;
  font-family: system-ui, -apple-system, sans-serif;
  line-height: 1.6;
}

.blockdoc-title {
  margin-bottom: 1.5rem;
}

.blockdoc-block {
  margin-bottom: 1.5rem;
}

.blockdoc-image {
  max-width: 100%;
  height: auto;
}

.blockdoc-figure {
  margin: 0 0 1.5rem 0;
}

.blockdoc-caption {
  font-size: 0.9rem;
  color: #666;
  text-align: center;
  margin-top: 0.5rem;
}

.blockdoc-quote {
  border-left: 4px solid #ccc;
  padding-left: 1rem;
  font-style: italic;
  margin: 0;
}

.blockdoc-attribution {
  display: block;
  text-align: right;
  font-style: normal;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.blockdoc-pre {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 1rem;
  overflow-x: auto;
}

.blockdoc-code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.9rem;
}

.blockdoc-divider {
  border: 0;
  border-top: 1px solid #eee;
  margin: 2rem 0;
}

.blockdoc-embed-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
}

.blockdoc-embed-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

## Security Notes

The HTML renderer uses sanitization to prevent XSS attacks:

- Text content is processed through the markdown library, which handles escaping
- URLs are sanitized to prevent javascript: protocol and other unsafe URLs
- HTML content is sanitized to remove unsafe tags and attributes