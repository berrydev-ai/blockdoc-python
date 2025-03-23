# Understanding BlockDoc Block Types

This tutorial provides a comprehensive guide to all the block types available in BlockDoc, including their properties, use cases, and examples.

## Table of Contents

1. [Text Blocks](#text-blocks)
2. [Heading Blocks](#heading-blocks)
3. [Image Blocks](#image-blocks)
4. [Code Blocks](#code-blocks)
5. [List Blocks](#list-blocks)
6. [Quote Blocks](#quote-blocks)
7. [Embed Blocks](#embed-blocks)
8. [Divider Blocks](#divider-blocks)
9. [Custom Block Properties](#custom-block-properties)

## Text Blocks

Text blocks are the most common blocks in a document, representing paragraphs of text formatted with Markdown.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"text"` 
- `content`: Markdown-formatted text content

### Example

```python
from blockdoc import Block

text_block = Block.text(
    "introduction",
    "This is a paragraph with **bold text**, *italic text*, and [links](https://example.com).\n\nMarkdown allows for multiple paragraphs within a single text block."
)
```

### Rendering

- **HTML**: Renders as `<p>` tags with HTML formatted according to Markdown syntax
- **Markdown**: Preserves the original Markdown content

### Use Cases

- Regular paragraphs
- Rich text content with formatting
- Multi-paragraph sections

### Markdown Features Supported

- **Bold**: `**bold text**` or `__bold text__`
- **Italic**: `*italic text*` or `_italic text_`
- **Links**: `[link text](https://example.com)`
- **Inline Code**: `` `code` ``
- **Multiple Paragraphs**: Separate with blank lines
- **Line Breaks**: End a line with two spaces or `\n`
- **Strikethrough**: `~~strikethrough~~`

## Heading Blocks

Heading blocks represent section titles and subheadings in a document.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"heading"`
- `content`: The heading text
- `level` (required): Heading level, from 1 (highest) to 6 (lowest)

### Example

```python
from blockdoc import Block

# Main heading (h1)
heading1 = Block.heading("page-title", 1, "Document Title")

# Section heading (h2)
heading2 = Block.heading("section-1", 2, "First Section")

# Subsection heading (h3)
heading3 = Block.heading("subsection-1-1", 3, "Subsection")
```

### Rendering

- **HTML**: Renders as `<h1>` through `<h6>` tags, depending on the level
- **Markdown**: Renders with the corresponding number of `#` characters

### Use Cases

- Document titles
- Section headings
- Content organization and hierarchy

### Best Practices

- Use heading levels consistently and hierarchically
- Don't skip heading levels (e.g., don't follow an h2 with an h4)
- Keep heading text concise
- Use semantic IDs that reflect the heading content

## Image Blocks

Image blocks represent visual content with a URL source, alternative text, and an optional caption.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"image"`
- `content`: Usually empty or used for additional information
- `url` (required): The image URL
- `alt` (required): Alternative text for accessibility
- `caption` (optional): Image caption

### Example

```python
from blockdoc import Block

# Basic image
basic_image = Block.image(
    "hero-image",
    "https://example.com/image.jpg",
    "Photo of mountains at sunset"
)

# Image with caption
captioned_image = Block.image(
    "diagram",
    "https://example.com/diagram.png",
    "System architecture diagram",
    "Figure 1: System Architecture Overview"
)
```

### Rendering

- **HTML**: Renders as an `<img>` element, with optional `<figure>` and `<figcaption>` for captioned images
- **Markdown**: Renders as Markdown image syntax `![alt](url)` with caption as text below

### Use Cases

- Photos and illustrations
- Charts and diagrams
- Screenshots
- Logos and icons

### Best Practices

- Always provide meaningful alt text for accessibility
- Use high-quality, optimized images
- Include captions for images that need additional context

## Code Blocks

Code blocks contain programming code with syntax highlighting based on the specified language.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"code"`
- `content`: The code content, preserving whitespace and indentation
- `language` (required): Programming language for syntax highlighting

### Example

```python
from blockdoc import Block

python_code = Block.code(
    "example-code",
    "python",
    """def hello_world():
    print("Hello, World!")
    
# Call the function
hello_world()"""
)

html_code = Block.code(
    "html-example",
    "html",
    """<!DOCTYPE html>
<html>
<head>
    <title>Example</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>"""
)
```

### Rendering

- **HTML**: Renders as a `<pre><code>` block with syntax highlighting
- **Markdown**: Renders as a fenced code block with language identifier (```python)

### Supported Languages

The code block supports any language recognized by the Pygments library, including but not limited to:

- Python
- JavaScript
- HTML
- CSS
- Java
- C/C++
- Ruby
- PHP
- Go
- Rust
- Shell/Bash
- SQL
- JSON
- YAML
- Markdown
- And many more...

Use `"plain"` for plain text without syntax highlighting.

### Use Cases

- Example code
- Configuration snippets
- Command-line instructions
- Data examples (JSON, XML, etc.)

### Best Practices

- Specify the correct language for proper syntax highlighting
- Use meaningful indentation and formatting
- Keep code examples concise and focused
- Include comments when necessary for clarity

## List Blocks

List blocks represent ordered (numbered) or unordered (bulleted) lists.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"list"`
- `content`: Usually empty
- `items` (required): Array of strings, each representing a list item
- `list_type` (required): Either `"ordered"` or `"unordered"`

### Example

```python
from blockdoc import Block

# Unordered list
feature_list = Block.list(
    "features",
    [
        "First feature with **bold text**",
        "Second feature with [link](https://example.com)",
        "Third feature with `code`"
    ],
    "unordered"
)

# Ordered list
steps_list = Block.list(
    "steps",
    [
        "First step",
        "Second step",
        "Third step"
    ],
    "ordered"
)
```

### Rendering

- **HTML**: Renders as `<ul>` or `<ol>` with `<li>` elements
- **Markdown**: Renders as Markdown list syntax (`-` or numbers)

### Use Cases

- Feature lists
- Steps in a process
- Pros and cons
- Table of contents
- Requirements

### Markdown in List Items

Each list item supports Markdown formatting:

- Bold, italic, and other text formatting
- Links
- Inline code
- Other inline Markdown elements

### Best Practices

- Use ordered lists for sequential steps
- Use unordered lists for non-sequential items
- Keep list items concise
- Use consistent formatting across list items
- Use nested list items when appropriate for hierarchy

## Quote Blocks

Quote blocks represent quotations or excerpts, optionally with attribution.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"quote"`
- `content`: The quoted text, can contain Markdown
- `attribution` (optional): Source of the quote

### Example

```python
from blockdoc import Block

# Simple quote
simple_quote = Block.quote(
    "einstein-quote",
    "Imagination is more important than knowledge."
)

# Quote with attribution
attributed_quote = Block.quote(
    "design-quote",
    "Design is not just what it looks like and feels like. Design is how it works.",
    "Steve Jobs"
)
```

### Rendering

- **HTML**: Renders as a `<blockquote>` element with optional `<cite>` for attribution
- **Markdown**: Renders with `>` prefix and attribution as text

### Use Cases

- Testimonials
- Important statements
- Literary quotes
- Excerpts from other sources

### Best Practices

- Use quotes for exact wording from sources
- Always include attribution for others' words
- Use Markdown formatting within quotes when needed
- Keep quotes concise and focused

## Embed Blocks

Embed blocks represent embedded content from external sources, such as videos or social media posts.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"embed"`
- `content`: Usually empty or used for additional information
- `url` (required): URL of the embedded content
- `embed_type` (required): Type of embed (`"youtube"`, `"twitter"`, or `"generic"`)
- `caption` (optional): Caption for the embedded content

### Example

```python
from blockdoc import Block

# YouTube video
youtube_embed = Block.embed(
    "tutorial-video",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "youtube",
    "Video tutorial on using BlockDoc"
)

# Twitter post
twitter_embed = Block.embed(
    "tweet",
    "https://twitter.com/user/status/123456789",
    "twitter",
    "Announcement tweet"
)

# Generic iframe embed
generic_embed = Block.embed(
    "map",
    "https://www.google.com/maps/embed?pb=!1m18!1m12!...",
    "generic",
    "Office location"
)
```

### Rendering

- **HTML**: Renders as appropriate embed code (iframe for YouTube, Twitter widget, etc.)
- **Markdown**: Renders as a link, since Markdown doesn't support embeds

### Supported Embed Types

1. **YouTube**
   - Automatically extracts video ID from various YouTube URL formats
   - Renders as a responsive iframe

2. **Twitter**
   - Embeds a Twitter post using Twitter's widget
   - Loads Twitter's JavaScript for interactive features

3. **Generic**
   - Creates a standard iframe for embedding any content
   - Use for maps, forms, or other iframe-compatible content

### Use Cases

- Instructional videos
- Social media content
- Interactive maps
- Live demos
- External content integration

### Best Practices

- Choose the appropriate embed type for the content
- Always provide a descriptive caption
- Consider fallback content for Markdown rendering
- Be aware of privacy implications of third-party embeds

## Divider Blocks

Divider blocks represent horizontal separators between content sections.

### Properties

- `id` (required): A unique identifier for the block
- `type`: Always `"divider"`
- `content`: Usually empty

### Example

```python
from blockdoc import Block

divider = Block.divider("section-break")
```

### Rendering

- **HTML**: Renders as an `<hr>` element
- **Markdown**: Renders as `---`

### Use Cases

- Separating content sections
- Indicating thematic breaks
- Creating visual separation

### Best Practices

- Use sparingly to avoid excessive visual breaks
- Place between logical content sections
- Use meaningful IDs that indicate the purpose of the divider

## Custom Block Properties

All block types support additional custom properties for special use cases.

### Adding Custom Properties

```python
from blockdoc import Block

# Add custom properties to a text block
custom_block = Block({
    "id": "special-text",
    "type": "text",
    "content": "This block has custom properties.",
    "customProp1": "value1",
    "customProp2": 42,
    "customProp3": {
        "nested": "object"
    }
})

# Or use update method on an existing block
normal_block = Block.text("intro", "Introduction text")
normal_block.update({
    "customFlag": True,
    "customData": ["array", "of", "values"]
})
```

### Use Cases for Custom Properties

1. **Frontend rendering hints**
   - `background_color`: Specify a background color
   - `theme`: Specify a theme variant

2. **Tracking and analytics**
   - `created_at`: Timestamp for creation
   - `updated_at`: Timestamp for updates
   - `created_by`: Author identifier

3. **Processing instructions**
   - `processing_hints`: Instructions for renderers
   - `translation_status`: Track translation state

4. **Application-specific metadata**
   - Domain-specific properties
   - Integration information

### Best Practices for Custom Properties

- Use custom properties sparingly and with purpose
- Document all custom properties in your application
- Prefer snake_case naming in Python (e.g., `custom_property`)
- Consider performance implications for large nested objects
- Don't use custom properties to work around core structure

## Conclusion

BlockDoc's block types provide a flexible yet structured approach to content representation. By understanding the properties and best practices for each block type, you can create rich, structured documents that are easy to manipulate and render in different formats.

For more advanced topics, check out the [LLM Integration Tutorial](llm-integration.md) to learn how to use BlockDoc with language models.