# BlockDoc Examples

This directory contains examples demonstrating how to use BlockDoc in different scenarios.

## Available Examples

### Basic Example

The [basic_example.py](basic_example.py) script demonstrates fundamental BlockDoc functionality:

- Creating a document with various block types
- Working with the Block factory methods
- Validating documents against the schema
- Rendering to HTML and Markdown
- Updating block content
- Saving and loading documents

Run it with:

```bash
python examples/basic_example.py
```

### Simple Blog

The [simple-blog](simple-blog/) directory contains a more complete example of creating a blog using BlockDoc:

- Structured blog post creation
- Multiple rendering formats
- Template integration
- Content management workflow
- See the README in that directory for more details

### LLM Integration

The [llm-integration](llm-integration/) directory demonstrates how to use BlockDoc with Language Models:

- Content generation with LLMs
- Targeted updates to specific blocks
- Content enhancement workflows
- Translation examples
- See the README in that directory for more details

## Running the Examples

1. Make sure you have BlockDoc installed:

```bash
pip install blockdoc
```

2. Navigate to the BlockDoc root directory:

```bash
cd path/to/blockdoc-python
```

3. Run an example:

```bash
python examples/basic_example.py
```

## Output

Most examples generate output files in an `output` directory within the example directory. These typically include:

- JSON files containing the BlockDoc document structure
- HTML files showing rendered output
- Markdown files showing rendered output
- Any other relevant output files

## Creating Your Own Examples

If you create interesting examples using BlockDoc, we'd love to see them! Consider contributing to the project by submitting a pull request with your example.