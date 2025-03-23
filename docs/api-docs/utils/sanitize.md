# Sanitization Utilities API Reference

The sanitization utilities provide functions for securing content in BlockDoc documents, particularly when rendering to HTML.

## Import

```python
from blockdoc.utils.sanitize import sanitize_html, sanitize_url
```

## Functions

### `sanitize_html(html_str)`

Sanitizes HTML content to remove potentially dangerous elements and attributes.

**Parameters:**

- `html_str` (str): HTML string to sanitize

**Returns:**

- `str`: Sanitized HTML string

**Example:**

```python
from blockdoc.utils.sanitize import sanitize_html

unsafe_html = '<script>alert("XSS")</script><p>Hello <strong>world</strong></p>'
safe_html = sanitize_html(unsafe_html)
# Result: '<p>Hello <strong>world</strong></p>'
```

### `sanitize_url(url_str)`

Sanitizes a URL to prevent javascript: protocol and other unsafe URL schemes.

**Parameters:**

- `url_str` (str): URL string to sanitize

**Returns:**

- `str`: Sanitized URL string

**Example:**

```python
from blockdoc.utils.sanitize import sanitize_url

unsafe_url = 'javascript:alert("XSS")'
safe_url = sanitize_url(unsafe_url)
# Result: ''

normal_url = 'https://example.com'
result = sanitize_url(normal_url)
# Result: 'https://example.com'
```

## Security Measures

### HTML Sanitization

The `sanitize_html` function implements several security measures:

1. **Tag Filtering**: Allows only safe tags such as `<p>`, `<a>`, `<strong>`, etc.
2. **Attribute Filtering**: Removes dangerous attributes like `onclick`, `onerror`, etc.
3. **Protocol Checking**: Ensures links use safe protocols (http, https, mailto, etc.)
4. **CSS Sanitization**: Removes potentially dangerous CSS properties and url() references

### URL Sanitization

The `sanitize_url` function implements these security measures:

1. **Protocol Checking**: Ensures URLs use safe protocols
2. **Format Validation**: Checks for malformed URLs
3. **Encoding Conversion**: Handles URL encoding to prevent bypass attacks

## Implementation Details

The sanitization functions use a whitelist approach, only allowing known-safe content through rather than trying to detect and block malicious content. This is a more secure approach.

### Allowed HTML Tags

The HTML sanitizer allows a subset of HTML tags that are considered safe for rendering:

- Structural: `p`, `div`, `span`, `br`, `hr`
- Headings: `h1`, `h2`, `h3`, `h4`, `h5`, `h6`
- Formatting: `b`, `strong`, `i`, `em`, `u`, `s`, `strike`, `sup`, `sub`
- Lists: `ul`, `ol`, `li`, `dl`, `dt`, `dd`
- Images: `img` (with src and alt attributes)
- Links: `a` (with href and title attributes)
- Tables: `table`, `thead`, `tbody`, `tr`, `th`, `td`
- Semantic: `figure`, `figcaption`, `blockquote`, `cite`, `code`, `pre`

### Allowed URL Protocols

The URL sanitizer allows a limited set of protocols:

- Web: `http`, `https`
- Email: `mailto`
- Phone: `tel`
- Other safe protocols: `ftp`, `data` (with restrictions)

## Usage in BlockDoc

These sanitization functions are used extensively in the HTML renderer to ensure that user-provided content is safe to render. They are called whenever potentially unsafe content is included in the output.

## Best Practices

1. **Always Sanitize User Content**: Use these utilities for any content that comes from external sources
2. **Apply Sanitization as Late as Possible**: Sanitize at render time rather than at storage time
3. **Use Both Functions**: Apply both HTML and URL sanitization when appropriate
4. **Don't Roll Your Own**: Security is challenging - use these tested functions rather than implementing your own

## Complete Example

```python
from blockdoc import BlockDocDocument, Block
from blockdoc.utils.sanitize import sanitize_html, sanitize_url

# Input from untrusted source
user_content = """
<p>This is an example with <script>alert('XSS')</script> unsafe content.</p>
<img src="javascript:alert('XSS')" alt="Image">
"""

user_url = "javascript:alert('XSS')"

# Sanitize the content before using it
safe_content = sanitize_html(user_content)
safe_url = sanitize_url(user_url)

# Create a BlockDoc document with the sanitized content
doc = BlockDocDocument({
    "title": "User Content Example",
})

doc.add_block(Block.text("user-content", safe_content))

# If the URL is not empty after sanitization, add an image block
if safe_url:
    doc.add_block(Block.image("user-image", safe_url, "User provided image"))

# Render to HTML (the renderer also applies sanitization)
html = doc.render_to_html()
```