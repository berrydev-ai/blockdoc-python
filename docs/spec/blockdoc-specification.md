# BlockDoc Specification

**Version:** 1.0.1
**Status:** Stable
**Maintainer:** BlockDoc Team

## Overview

BlockDoc is a structured content format designed for creating, managing, and rendering content in a way that is optimized for both human authors and language models (LLMs). It provides a simple, intuitive structure that makes content easier to manipulate, update, and transform programmatically.

## Document Structure

A BlockDoc document consists of a top-level `article` object with the following properties:

```json
{
  "article": {
    "title": "Document Title",
    "metadata": {
      "author": "Author Name",
      "publishedDate": "2025-03-23T10:00:00Z",
      "tags": ["tag1", "tag2"]
    },
    "blocks": [
      // Array of content blocks
    ]
  }
}
```

### Required Properties

- `title` (string): The document title
- `blocks` (array): An array of content blocks

### Optional Properties

- `metadata` (object): Additional document metadata
  - `author` (string): Document author
  - `publishedDate` (string): ISO 8601 date-time format
  - `tags` (array of strings): Content tags
  - Any other custom metadata properties

## Block Structure

Each block in the `blocks` array represents a discrete unit of content with the following structure:

```json
{
  "id": "unique-semantic-id",
  "type": "text",
  "content": "Content of the block, formatted according to the block type."
}
```

### Required Properties for All Blocks

- `id` (string): A unique, semantic identifier for the block (e.g., "introduction", "section-1-heading")
- `type` (string): The block type (e.g., "text", "heading")
- `content` (string): The content of the block, interpreted based on the block type

### Block Types

BlockDoc supports the following core block types:

#### 1. Text

Text blocks contain Markdown-formatted text.

```json
{
  "id": "intro-paragraph",
  "type": "text",
  "content": "This is **formatted** text with [links](https://example.com)."
}
```

#### 2. Heading

Heading blocks represent section titles with a specified level (1-6).

```json
{
  "id": "section-title",
  "type": "heading",
  "level": 2,
  "content": "Section Title"
}
```

**Additional Required Properties:**
- `level` (integer): Heading level, from 1 (highest) to 6 (lowest)

#### 3. Image

Image blocks represent visual content with a URL, alt text, and optional caption.

```json
{
  "id": "hero-image",
  "type": "image",
  "content": "",
  "url": "https://example.com/image.jpg",
  "alt": "Description of the image",
  "caption": "Optional image caption"
}
```

**Additional Required Properties:**
- `url` (string): The image URL
- `alt` (string): Alternative text for accessibility

**Optional Properties:**
- `caption` (string): Image caption

#### 4. Code

Code blocks contain programming code with syntax highlighting.

```json
{
  "id": "example-code",
  "type": "code",
  "language": "python",
  "content": "def hello_world():\n    print(\"Hello, World!\")"
}
```

**Additional Required Properties:**
- `language` (string): Programming language for syntax highlighting

#### 5. List

List blocks represent ordered or unordered lists.

```json
{
  "id": "feature-list",
  "type": "list",
  "list_type": "unordered",
  "items": [
    "First item",
    "Second item with **formatting**",
    "Third item with [link](https://example.com)"
  ]
}
```

**Additional Required Properties:**
- `items` (array of strings): List items, supporting Markdown formatting
- `list_type` (string): Either "ordered" or "unordered"

#### 6. Quote

Quote blocks represent quotations with optional attribution.

```json
{
  "id": "important-quote",
  "type": "quote",
  "content": "This is a quotation that might span multiple lines.",
  "attribution": "Source of the quote"
}
```

**Optional Properties:**
- `attribution` (string): Quote attribution

#### 7. Embed

Embed blocks represent embedded content from external sources.

```json
{
  "id": "video-embed",
  "type": "embed",
  "content": "",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "embed_type": "youtube",
  "caption": "Optional caption for the embedded content"
}
```

**Additional Required Properties:**
- `url` (string): URL of the embedded content
- `embed_type` (string): Type of embed ("youtube", "twitter", or "generic")

**Optional Properties:**
- `caption` (string): Caption for the embedded content

#### 8. Divider

Divider blocks represent horizontal separators between content sections.

```json
{
  "id": "section-divider",
  "type": "divider",
  "content": ""
}
```

## Naming Conventions

### Block IDs

Block IDs should be:
- Unique within the document
- Semantic in nature (describing the content's purpose)
- Lowercase with hyphens for separating words
- Composed of alphanumeric characters, hyphens, and underscores only

Examples of good block IDs:
- `introduction`
- `key-features`
- `section-1-heading`
- `code-example-python`

## Property Naming

BlockDoc follows a mixed naming convention to support interoperability:

- Python implementation primarily uses snake_case (`list_type`, `embed_type`)
- For compatibility with JavaScript, camelCase versions of properties (`listType`, `embedType`) are also recognized

## Best Practices

### Document Organization

1. **Semantic Structure**: Organize blocks in a logical flow with meaningful IDs
2. **Granularity**: Divide content into reasonably sized blocks for targeted modification
3. **Self-Contained Blocks**: Each block should function as a coherent unit of content

### Working with LLMs

1. **Clear Instructions**: When using LLMs to modify content, identify blocks by their semantic IDs
2. **Targeted Updates**: Request updates to specific blocks rather than the entire document
3. **Context Preservation**: Provide surrounding context when necessary for coherent updates

### Content Authoring

1. **Markdown in Text Blocks**: Use Markdown for formatting text content
2. **Semantic Headings**: Use heading levels appropriately to maintain document hierarchy
3. **Accessibility**: Always provide alt text for images and appropriate captions

## Extension Guidelines

BlockDoc can be extended with custom block types for domain-specific use cases:

1. Define a new block type with a descriptive name
2. Document the block type's required and optional properties
3. Implement rendering logic for the custom block type
4. Consider backward compatibility with core BlockDoc renderers

## Schema Validation

BlockDoc documents can be validated against the JSON schema available at:
- Python: `blockdoc/schema/blockdoc.schema.json`
- NPM: `blockdoc/dist/schema/blockdoc.schema.json`

## Use Cases

BlockDoc is particularly well-suited for:

1. **Content Management Systems**: Structured storage with granular update capability
2. **Documentation**: Technical documentation with code examples and structured sections
3. **LLM-powered applications**: Content generation and modification with semantic structure
4. **Blogs and Articles**: Structured content with rich multimedia support
5. **Educational Content**: Lessons and tutorials with mixed content types

## Comparison with Other Formats

| Feature | BlockDoc | Markdown | JSON | HTML |
|---------|----------|----------|------|------|
| Structured | ✓ | ✗ | ✓ | ✓ |
| Human-readable | ✓ | ✓ | ✗ | ✗ |
| Semantic IDs | ✓ | ✗ | ✗ | ✓ |
| Block-level targeting | ✓ | ✗ | ✓ | ✓ |
| Metadata support | ✓ | ✗ | ✓ | ✓ |
| Markdown in content | ✓ | ✓ | ✗ | ✗ |
| LLM-friendly | ✓ | ✓ | ✗ | ✗ |
| Database-ready | ✓ | ✗ | ✓ | ✗ |

## Version History

- **1.0.0** (2025-03-23): Initial stable release
- **0.9.0** (2025-02-15): Beta release with core block types
- **0.5.0** (2025-01-10): Alpha release for testing