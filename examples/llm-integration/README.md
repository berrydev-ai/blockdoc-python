# BlockDoc LLM Integration Examples

This directory contains examples demonstrating how to use BlockDoc with Language Models (LLMs) for content generation and manipulation.

## Features

- Generate complete documents with LLMs
- Update specific blocks in a document
- Structured content creation with semantic blocks
- Demonstrations of prompt engineering for block-specific content

## Getting Started

### Prerequisites

- Python 3.8 or higher
- BlockDoc package installed
- API key for an LLM provider (OpenAI, Anthropic, etc.)

### Setting Up

1. Set your LLM API key as an environment variable:

```bash
# For OpenAI
export OPENAI_API_KEY="your-api-key"

# For Anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

2. Edit the `llm_content_generator.py` file to uncomment the section for your preferred LLM provider.

### Running the Example

1. Navigate to the BlockDoc root directory:

```bash
cd path/to/blockdoc-python
```

2. Generate a new article:

```bash
python examples/llm-integration/llm_content_generator.py --title "My LLM-Generated Article" --topic "structured content for AI applications"
```

3. Update a specific block in an existing article:

```bash
python examples/llm-integration/llm_content_generator.py --update --input examples/llm-integration/output/my-llm-generated-article.json --block-id introduction --instruction "Make it more concise and add a statistic about AI content generation"
```

## Command-line Options

### For Article Generation

- `--title`: Specify the article title (default: "BlockDoc: A Modern Approach to Structured Content")
- `--topic`: Specify the article topic (default: "structured content formats for modern applications")
- `--output-dir`: Directory to save the generated files (default: "./output")

### For Block Updates

- `--update`: Enable update mode
- `--input`: Path to the JSON file containing the document to update
- `--block-id`: ID of the block to update
- `--instruction`: Instructions for updating the block
- `--output-dir`: Directory to save the updated files (default: "./output")

## LLM Integration Approaches

This example demonstrates several key approaches for integrating BlockDoc with LLMs:

1. **Document Generation**: Creating complete documents with a structured approach
2. **Targeted Updates**: Updating specific blocks without regenerating the entire document
3. **Block-Specific Prompts**: Crafting prompts based on block type and context
4. **Parsing Structured Responses**: Converting LLM responses into structured BlockDoc blocks

## Extending the Example

You can extend this example in various ways:

1. **Additional Block Types**: Add support for generating and updating more block types
2. **Content Plans**: Implement a planning phase before generation
3. **Content Enhancement**: Add capabilities for enhancing existing content
4. **Bulk Operations**: Support batch operations on multiple blocks
5. **Interactive Editing**: Build an interactive editing workflow

## Making It Work with Your LLM Provider

The example includes commented sections for both OpenAI and Anthropic. To use with your preferred provider:

1. Uncomment the appropriate section in `llm_content_generator.py`
2. Install the required package (`pip install openai` or `pip install anthropic`)
3. Set your API key
4. Adjust parameters like model name as needed

## Output Files

The generator creates three files for each article:

1. `[title-slug].json`: The BlockDoc document structure in JSON format
2. `[title-slug].html`: The article rendered as an HTML page with basic styling
3. `[title-slug].md`: The article rendered as Markdown with YAML frontmatter

For updates, it creates:

1. `updated_[filename].json`: The updated document
2. `updated_[filename].html`: HTML preview of the updated document

## Best Practices for Prompt Engineering

When working with BlockDoc and LLMs, consider these best practices:

1. **Block-Specific Prompts**: Customize prompts based on block type
2. **Clear Instructions**: Be specific about the desired format and content
3. **Context Preservation**: Include surrounding context for coherent updates
4. **Response Parsing**: Implement robust parsing for structured responses
5. **Validation**: Always validate the document after LLM operations

## Learn More

- Explore the [BlockDoc Documentation](../../docs/) for more details on the API
- Check out the [LLM Integration Tutorial](../../docs/tutorials/llm-integration.md) for an in-depth guide