# BlockDoc Simple Blog Example

This example demonstrates how to use BlockDoc to create and manage blog posts.

## Features

- Generate blog posts with a variety of block types
- Render blog posts to HTML, Markdown, and JSON
- Load blog structure from JSON templates
- Command-line interface for blog post generation

## Getting Started

### Prerequisites

- Python 3.8 or higher
- BlockDoc package installed

### Running the Example

1. Navigate to the BlockDoc root directory:

```bash
cd path/to/blockdoc-python
```

2. Run the blog generator with default settings:

```bash
python examples/simple-blog/blog_generator.py
```

This will create a sample blog post with default content and save it to the `examples/simple-blog/output` directory.

### Command-line Options

The blog generator supports several command-line options:

```bash
python examples/simple-blog/blog_generator.py --title "My Blog Post" --author "Your Name" --output-dir "./my-output"
```

Available options:

- `--title`: Specify the blog post title (default: "BlockDoc Blog Example")
- `--author`: Specify the blog post author (default: "BlockDoc Team")
- `--content`: Path to a JSON file containing the blog content structure
- `--output-dir`: Directory to save the generated files (default: "./output")

### Using a Custom Content Structure

You can define your blog post structure in a JSON file and use it with the `--content` option:

```bash
python examples/simple-blog/blog_generator.py --content "examples/simple-blog/sample_content.json"
```

## Content Structure

The JSON content structure should be an array of block definitions, each with at least a `type` and `id` property:

```json
[
  {
    "type": "text",
    "id": "introduction",
    "content": "This is the introduction paragraph."
  },
  {
    "type": "heading",
    "id": "section-1",
    "level": 2,
    "content": "First Section"
  },
  {
    "type": "list",
    "id": "key-points",
    "items": ["Point 1", "Point 2", "Point 3"],
    "list_type": "unordered"
  }
]
```

See the `sample_content.json` file for a complete example.

## Output Files

The generator creates three files for each blog post:

1. `[title-slug].json`: The BlockDoc document structure in JSON format
2. `[title-slug].html`: The blog post rendered as an HTML page with basic styling
3. `[title-slug].md`: The blog post rendered as Markdown with YAML frontmatter

## Using in Your Projects

This example can be adapted for various content creation workflows:

1. **Content Management System**: Use BlockDoc as the storage format for a CMS
2. **Static Site Generator**: Generate blog posts for static sites like Hugo or Jekyll
3. **LLM-powered Blogging**: Use LLMs to generate content in BlockDoc format
4. **Interactive Editors**: Build editors that save content in BlockDoc format

## Next Steps

- Explore the [BlockDoc Documentation](../../docs/) for more details on the API
- Check out the [LLM Integration Example](../llm-integration/) to see how to use BlockDoc with language models