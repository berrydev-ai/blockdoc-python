# BlockDocDocument Class API Reference

The `BlockDocDocument` class is the core class for creating, manipulating, and rendering BlockDoc documents.

## Import

```python
from blockdoc import BlockDocDocument
```

## Constructor

### `BlockDocDocument(options)`

Creates a new BlockDoc document.

**Parameters:**

- `options` (dict): Document initialization options
  - `title` (str): Document title
  - `metadata` (dict, optional): Optional document metadata
  - `blocks` (list, optional): Initial blocks to add

**Raises:**

- `ValueError`: If title is not provided

**Example:**

```python
doc = BlockDocDocument({
    "title": "My First BlockDoc Document",
    "metadata": {
        "author": "Your Name",
        "publishedDate": "2025-03-23T10:00:00Z",
        "tags": ["blockdoc", "example", "tutorial"]
    }
})
```

## Instance Methods

### `validate()`

Validates the document against the BlockDoc schema.

**Returns:**

- `bool`: True if valid

**Raises:**

- `ValueError`: If validation fails

**Example:**

```python
try:
    doc.validate()
    print("Document is valid!")
except ValueError as e:
    print(f"Validation error: {str(e)}")
```

### `add_block(block_data)`

Adds a block to the document.

**Parameters:**

- `block_data` (dict or Block): Block data or Block instance

**Returns:**

- `Block`: The created block

**Raises:**

- `ValueError`: If block with the same ID already exists

**Example:**

```python
from blockdoc import Block

# Add using a Block instance
doc.add_block(Block.text("intro", "Welcome to my first BlockDoc document."))

# Add using a dictionary
doc.add_block({
    "id": "explanation",
    "type": "text",
    "content": "This is a **formatted** paragraph with a [link](https://example.com)."
})
```

### `insert_block(block_data, position)`

Inserts a block at a specific position.

**Parameters:**

- `block_data` (dict or Block): Block data or Block instance
- `position` (int): Position to insert at

**Returns:**

- `Block`: The created block

**Raises:**

- `ValueError`: If block with the same ID already exists

**Example:**

```python
# Insert a block at position 0 (beginning of document)
doc.insert_block(Block.heading("title", 1, "Document Title"), 0)
```

### `get_block(id)`

Gets a block by ID.

**Parameters:**

- `id` (str): Block ID

**Returns:**

- `dict` or `None`: The block dictionary or None if not found

**Example:**

```python
intro_block = doc.get_block("intro")
if intro_block:
    print(f"Found block: {intro_block['content']}")
else:
    print("Block not found")
```

### `update_block(id, updates)`

Updates a block by ID.

**Parameters:**

- `id` (str): Block ID
- `updates` (dict): Properties to update

**Returns:**

- `dict`: The updated block

**Raises:**

- `ValueError`: If block with the ID doesn't exist

**Example:**

```python
doc.update_block("intro", {
    "content": "This is the updated introduction paragraph."
})
```

### `remove_block(id)`

Removes a block by ID.

**Parameters:**

- `id` (str): Block ID

**Returns:**

- `bool`: True if removed, False if not found

**Example:**

```python
if doc.remove_block("unwanted-block"):
    print("Block removed successfully")
else:
    print("Block not found")
```

### `move_block(id, new_position)`

Moves a block to a new position.

**Parameters:**

- `id` (str): Block ID
- `new_position` (int): New position

**Returns:**

- `bool`: True if moved, False if not found

**Raises:**

- `ValueError`: If new_position is invalid

**Example:**

```python
doc.move_block("intro", 2)  # Move the intro block to the third position
```

### `render_to_html()`

Renders the document to HTML.

**Returns:**

- `str`: HTML representation

**Example:**

```python
html = doc.render_to_html()
with open("document.html", "w") as f:
    f.write(html)
```

### `render_to_markdown()`

Renders the document to Markdown.

**Returns:**

- `str`: Markdown representation

**Example:**

```python
markdown = doc.render_to_markdown()
with open("document.md", "w") as f:
    f.write(markdown)
```

### `to_dict()`

Exports the document as a dictionary.

**Returns:**

- `dict`: Document as dictionary

**Example:**

```python
doc_dict = doc.to_dict()
```

### `to_json(indent=2)`

Exports the document as a JSON string.

**Parameters:**

- `indent` (int, optional): JSON indentation level, defaults to 2

**Returns:**

- `str`: Document as JSON string

**Example:**

```python
json_str = doc.to_json()
with open("document.json", "w") as f:
    f.write(json_str)
```

## Static Methods

### `from_dict(data)`

Creates a BlockDoc document from a dictionary.

**Parameters:**

- `data` (dict): Document data

**Returns:**

- `BlockDocDocument`: New document instance

**Raises:**

- `ValueError`: If data is invalid

**Example:**

```python
doc_dict = {
    "article": {
        "title": "My Document",
        "metadata": {"author": "Your Name"},
        "blocks": [
            {"id": "intro", "type": "text", "content": "Introduction paragraph."}
        ]
    }
}

doc = BlockDocDocument.from_dict(doc_dict)
```

### `from_json(json_str)`

Creates a BlockDoc document from a JSON string.

**Parameters:**

- `json_str` (str): JSON string

**Returns:**

- `BlockDocDocument`: New document instance

**Raises:**

- `ValueError`: If JSON is invalid

**Example:**

```python
with open("document.json", "r") as f:
    json_str = f.read()

doc = BlockDocDocument.from_json(json_str)
```

## Complete Example

```python
from blockdoc import BlockDocDocument, Block

# Create a new document
doc = BlockDocDocument({
    "title": "Getting Started with BlockDoc",
    "metadata": {
        "author": "BlockDoc Team",
        "publishedDate": "2025-03-23T10:00:00Z",
        "tags": ["blockdoc", "tutorial", "content"]
    }
})

# Add blocks
doc.add_block(Block.text(
    "intro",
    "Welcome to **BlockDoc**, a simple yet powerful format for structured content."
))

doc.add_block(Block.heading(
    "section-1",
    2,
    "Getting Started"
))

doc.add_block(Block.text(
    "para-1",
    "This is a paragraph with some **bold text** and a [link](https://example.com)."
))

doc.add_block(Block.code(
    "example-code",
    "python",
    "from blockdoc import BlockDocDocument, Block\n\ndoc = BlockDocDocument({\n    \"title\": \"Example\"\n})"
))

# Validate the document
doc.validate()

# Render to different formats
html = doc.render_to_html()
markdown = doc.render_to_markdown()
json_str = doc.to_json()

# Update a block
doc.update_block("para-1", {
    "content": "This paragraph has been updated with new content."
})

# Remove a block
doc.remove_block("example-code")

# Add a new block and move it
doc.add_block(Block.list(
    "feature-list",
    ["Feature 1", "Feature 2", "Feature 3"],
    "unordered"
))
doc.move_block("feature-list", 1)  # Move it to the second position
```