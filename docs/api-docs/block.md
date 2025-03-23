# Block Class API Reference

The `Block` class represents a single content block within a BlockDoc document.

## Import

```python
from blockdoc import Block
```

## Constructor

### `Block(data)`

Creates a new Block instance.

**Parameters:**

- `data` (dict): Block data containing at least the following required properties:
  - `id` (str): A unique, semantic identifier for the block
  - `type` (str): The block type, one of the allowed types
  - `content` (str, optional): The content of the block, defaults to empty string
  - Additional type-specific properties as required

**Raises:**

- `ValueError`: If the block is missing required properties or has an invalid type

**Example:**

```python
block = Block({
    "id": "introduction",
    "type": "text",
    "content": "This is a **formatted** introduction paragraph."
})
```

## Constants

### `ALLOWED_TYPES`

A list of allowed block types.

```python
ALLOWED_TYPES = [
    'text',
    'heading',
    'image',
    'code',
    'list',
    'quote',
    'embed',
    'divider',
]
```

### `TYPE_REQUIREMENTS`

A dictionary mapping block types to their required properties.

```python
TYPE_REQUIREMENTS = {
    'heading': ['level'],
    'code': ['language'],
    'image': ['url', 'alt'],
    'list': ['items', 'list_type'],
}
```

## Instance Methods

### `update(updates)`

Updates block properties with new values.

**Parameters:**

- `updates` (dict): Properties to update

**Returns:**

- `Block`: The updated block instance

**Notes:**

- Cannot change the block's `id` or `type`
- Any other property can be updated

**Example:**

```python
block.update({
    "content": "This is the updated content.",
    "custom_property": "custom value"
})
```

### `to_dict()`

Converts the block to a dictionary.

**Returns:**

- `dict`: The block as a dictionary

**Example:**

```python
block_dict = block.to_dict()
```

## Factory Methods

### `Block.text(id, content)`

Creates a text block.

**Parameters:**

- `id` (str): Block ID
- `content` (str): Markdown content

**Returns:**

- `Block`: A new text block instance

**Example:**

```python
text_block = Block.text("intro", "This is **formatted** text with [links](https://example.com).")
```

### `Block.heading(id, level, content)`

Creates a heading block.

**Parameters:**

- `id` (str): Block ID
- `level` (int): Heading level (1-6)
- `content` (str): Heading text

**Returns:**

- `Block`: A new heading block instance

**Example:**

```python
heading_block = Block.heading("section-title", 2, "Section Title")
```

### `Block.image(id, url, alt, caption=None)`

Creates an image block.

**Parameters:**

- `id` (str): Block ID
- `url` (str): Image URL
- `alt` (str): Alt text
- `caption` (str, optional): Optional caption

**Returns:**

- `Block`: A new image block instance

**Example:**

```python
image_block = Block.image(
    "hero-image", 
    "https://example.com/image.jpg", 
    "Example image", 
    "This is the caption"
)
```

### `Block.code(id, language, content)`

Creates a code block.

**Parameters:**

- `id` (str): Block ID
- `language` (str): Programming language
- `content` (str): Code content

**Returns:**

- `Block`: A new code block instance

**Example:**

```python
code_block = Block.code(
    "example-code", 
    "python", 
    "def hello_world():\n    print(\"Hello, World!\")"
)
```

### `Block.list(id, items, list_type='unordered')`

Creates a list block.

**Parameters:**

- `id` (str): Block ID
- `items` (list): List items
- `list_type` (str, optional): List type ("ordered" or "unordered"), defaults to "unordered"

**Returns:**

- `Block`: A new list block instance

**Example:**

```python
list_block = Block.list(
    "feature-list",
    [
        "First item",
        "Second item with **formatting**",
        "Third item with [link](https://example.com)"
    ],
    "unordered"
)
```

### `Block.quote(id, content, attribution=None)`

Creates a quote block.

**Parameters:**

- `id` (str): Block ID
- `content` (str): Quote content
- `attribution` (str, optional): Source attribution

**Returns:**

- `Block`: A new quote block instance

**Example:**

```python
quote_block = Block.quote(
    "important-quote",
    "This is a quotation that might span multiple lines.",
    "Source of the quote"
)
```

### `Block.embed(id, url, embed_type, caption=None)`

Creates an embed block.

**Parameters:**

- `id` (str): Block ID
- `url` (str): URL of embedded content
- `embed_type` (str): Type of embed ("youtube", "twitter", "generic")
- `caption` (str, optional): Optional caption

**Returns:**

- `Block`: A new embed block instance

**Example:**

```python
embed_block = Block.embed(
    "video-embed",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "youtube",
    "Optional caption"
)
```

### `Block.divider(id)`

Creates a divider block.

**Parameters:**

- `id` (str): Block ID

**Returns:**

- `Block`: A new divider block instance

**Example:**

```python
divider_block = Block.divider("section-divider")
```

## Complete Example

```python
from blockdoc import Block

# Create blocks using factory methods
text_block = Block.text(
    "introduction",
    "Welcome to **BlockDoc**, a simple yet powerful format for structured content."
)

heading_block = Block.heading(
    "section-title",
    2,
    "Section Title"
)

list_block = Block.list(
    "feature-list",
    [
        "First feature",
        "Second feature",
        "Third feature"
    ],
    "unordered"
)

# Create a block directly with the constructor
custom_block = Block({
    "id": "custom-block",
    "type": "text",
    "content": "This is a custom block with extra properties.",
    "custom_property": "custom value"
})

# Update a block
custom_block.update({
    "content": "Updated content"
})

# Convert a block to a dictionary
block_dict = custom_block.to_dict()
```