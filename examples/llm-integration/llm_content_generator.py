"""
BlockDoc LLM Content Generator

This example demonstrates using BlockDoc with Language Models (LLMs) to generate
and manipulate structured content.

Note: This is a demonstration example. You need to provide your own API key
and uncomment the appropriate sections to use with your preferred LLM provider.
"""

import argparse
import datetime
import os
import sys

# Add the parent directory to sys.path to import blockdoc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from blockdoc import Block, BlockDocDocument

# Uncomment and modify the section for your preferred LLM provider:

# # Option 1: OpenAI
# import openai
#
# # Set your API key
# # openai.api_key = os.environ.get("OPENAI_API_KEY")
#
# def generate_with_llm(prompt, max_tokens=800):
#     """Generate text using OpenAI's API"""
#     response = openai.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful content creation assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=max_tokens,
#         temperature=0.7
#     )
#     return response.choices[0].message.content

# # Option 2: Anthropic
# import anthropic
#
# # Initialize the client
# # client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
#
# def generate_with_llm(prompt, max_tokens=800):
#     """Generate text using Anthropic's API"""
#     response = client.messages.create(
#         model="claude-3-opus-20240229",
#         max_tokens=max_tokens,
#         temperature=0.7,
#         system="You are a helpful content creation assistant.",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.content[0].text


# For demonstration, we'll use a mock LLM function:
def generate_with_llm(prompt, max_tokens=800):
    """Mock LLM function that returns predefined responses based on the prompt"""
    if "introduction" in prompt.lower():
        return """BlockDoc is a powerful structured content format designed specifically for modern content workflows. 
        It combines the simplicity of block-based editing with the flexibility of structured data, making it ideal for both human authors and AI assistants.
        
        In this article, we'll explore how BlockDoc works, its key features, and why it's becoming the preferred format for content-heavy applications."""

    elif "benefits" in prompt.lower() or "advantages" in prompt.lower():
        return """1. **Semantic Structure**: Every block has a meaningful ID that describes its purpose
2. **Granular Control**: Update or replace specific sections without touching the rest
3. **LLM Optimization**: Perfect for AI-generated content and targeted updates
4. **Rendering Flexibility**: Output to HTML, Markdown, or custom formats
5. **Database Friendly**: Easy to store in document databases"""

    elif "code example" in prompt.lower():
        return """```python
from blockdoc import BlockDocDocument, Block

# Create a new document
doc = BlockDocDocument({
    "title": "My First Document",
    "metadata": {
        "author": "BlockDoc Team",
        "created": "2025-03-23"
    }
})

# Add some content blocks
doc.add_block(Block.heading("title", 1, "Welcome to BlockDoc"))
doc.add_block(Block.text("intro", "BlockDoc makes structured content **simple**."))

# Get the document as JSON
json_doc = doc.to_json()
print(json_doc)
```"""

    elif "use cases" in prompt.lower():
        return """BlockDoc is particularly well-suited for the following use cases:

1. **Content Management Systems**: Provides a structured yet flexible content model
2. **Documentation Sites**: Excellent for technical documentation with code examples
3. **LLM Applications**: Perfect for AI-assisted content generation and editing
4. **Blogs and Articles**: Rich content with mixed media types
5. **Educational Content**: Structured lessons with different content blocks"""

    elif "conclusion" in prompt.lower():
        return """As we've seen, BlockDoc offers a powerful yet simple approach to structured content. Its block-based architecture provides the perfect balance of flexibility and structure, making it adaptable to a wide range of content needs.

Whether you're building a CMS, working with LLMs, or simply need a better way to organize content, BlockDoc provides a solid foundation that grows with your needs.

Try BlockDoc today and experience the benefits of structured content that works for both humans and machines."""

    else:
        return "Content generated for: " + prompt


def create_article_with_llm(title, topic):
    """
    Create a complete BlockDoc article using an LLM

    Args:
        title (str): Article title
        topic (str): Article topic

    Returns:
        BlockDocDocument: The generated article
    """
    # Create a new document
    article = BlockDocDocument(
        {
            "title": title,
            "metadata": {
                "author": "BlockDoc LLM Assistant",
                "created": datetime.datetime.now().isoformat(),
                "topic": topic,
                "generated": True,
            },
        }
    )

    # Generate introduction
    intro_prompt = f"""Write an engaging introduction for an article titled "{title}" about {topic}.
    The introduction should be 2-3 paragraphs and explain what the article will cover.
    Use Markdown formatting where appropriate."""

    intro_content = generate_with_llm(intro_prompt)
    article.add_block(Block.text("introduction", intro_content))

    # Generate a section about benefits/features
    article.add_block(Block.heading("benefits", 2, f"Benefits of {topic}"))

    benefits_prompt = f"""Create a list of 4-6 key benefits or features of {topic}.
    Each item should be 1-2 sentences and start with a bold benefit name.
    Format as a markdown list."""

    benefits_content = generate_with_llm(benefits_prompt)

    # Parse the list items from the response
    benefits_items = []
    for line in benefits_content.split("\n"):
        line = line.strip()
        if line.startswith(("- ", "* ", "1. ")) and len(line) > 2:
            benefits_items.append(line[2:].strip())
        elif line and not line.startswith("#") and len(benefits_items) < 6:
            benefits_items.append(line)

    article.add_block(Block.list("benefits-list", benefits_items, "unordered"))

    # Generate a code example section
    article.add_block(Block.heading("code-example", 2, "Code Example"))

    code_prompt = f"""Create a Python code example related to {topic} using the BlockDoc library.
    The example should demonstrate creating a document with blocks and rendering it.
    Include comments to explain the code."""

    code_content = generate_with_llm(code_prompt)

    # Extract the code from markdown code blocks if present
    if "```" in code_content:
        code_parts = code_content.split("```")
        if len(code_parts) >= 3:
            # Get the content inside the code block
            code_block = code_parts[1]
            # Remove language identifier if present
            if code_block.startswith(("python", "py")):
                code_block = code_block[code_block.find("\n") + 1 :]
            code_content = code_block.strip()

    article.add_block(Block.code("example-code", "python", code_content))

    # Generate a use cases section
    article.add_block(Block.heading("use-cases", 2, "Use Cases"))

    use_cases_prompt = f"""Describe 4-5 practical use cases for {topic}.
    Explain how each use case benefits from the features of {topic}."""

    use_cases_content = generate_with_llm(use_cases_prompt)
    article.add_block(Block.text("use-cases-content", use_cases_content))

    # Add an image placeholder
    article.add_block(
        Block.image(
            "diagram",
            "https://placehold.co/800x400?text=Diagram:+" + topic.replace(" ", "+"),
            f"Diagram illustrating {topic}",
            f"Figure 1: Visual representation of {topic}",
        )
    )

    # Generate conclusion
    article.add_block(Block.heading("conclusion", 2, "Conclusion"))

    conclusion_prompt = f"""Write a conclusion for an article about {topic}.
    Summarize the key points and end with a call to action.
    Keep it to 2-3 paragraphs."""

    conclusion_content = generate_with_llm(conclusion_prompt)
    article.add_block(Block.text("conclusion-content", conclusion_content))

    return article


def update_block_with_llm(document, block_id, instruction):
    """
    Update a specific block using an LLM

    Args:
        document (BlockDocDocument): The document to update
        block_id (str): ID of the block to update
        instruction (str): Instructions for updating the block

    Returns:
        BlockDocDocument: The updated document
    """
    # Get the existing block
    block = document.get_block(block_id)
    if not block:
        raise ValueError(f"Block with ID '{block_id}' not found")

    block_type = block["type"]

    if block_type == "text":
        # Generate updated text content
        prompt = f"""Here is an existing text block:

{block["content"]}

Update this text according to these instructions: {instruction}

Preserve any markdown formatting that's appropriate. Return only the updated text."""

        updated_content = generate_with_llm(prompt)
        document.update_block(block_id, {"content": updated_content})

    elif block_type == "heading":
        # Generate updated heading
        prompt = f"""Here is an existing heading:

{block["content"]}

Update this heading according to these instructions: {instruction}

Keep it concise and clear. Return only the updated heading text."""

        updated_content = generate_with_llm(prompt)
        document.update_block(block_id, {"content": updated_content})

    elif block_type == "list":
        # Update list items
        items = block.get("items", [])
        items_text = "\n".join([f"- {item}" for item in items])

        prompt = f"""Here is an existing list:

{items_text}

Update this list according to these instructions: {instruction}

Return the updated list with each item on a new line starting with '- '."""

        updated_content = generate_with_llm(prompt)

        # Parse updated list items
        updated_items = []
        for line in updated_content.split("\n"):
            line = line.strip()
            if line.startswith(("- ", "* ", "• ")) and len(line) > 2:
                updated_items.append(line[2:].strip())

        if updated_items:
            document.update_block(block_id, {"items": updated_items})

    elif block_type == "code":
        # Update code content
        prompt = f"""Here is an existing code block in {block.get("language", "python")}:

{block["content"]}

Update this code according to these instructions: {instruction}

Return only the updated code, with no additional explanation."""

        updated_content = generate_with_llm(prompt)

        # Extract the code from markdown code blocks if present
        if "```" in updated_content:
            code_parts = updated_content.split("```")
            if len(code_parts) >= 3:
                # Get the content inside the code block
                code_block = code_parts[1]
                # Remove language identifier if present
                if code_block.startswith(("python", "py", block.get("language", ""))):
                    code_block = code_block[code_block.find("\n") + 1 :]
                updated_content = code_block.strip()

        document.update_block(block_id, {"content": updated_content})

    return document


def main():
    """
    Main function to run the example
    """
    parser = argparse.ArgumentParser(description="Generate content with LLMs and BlockDoc")
    parser.add_argument(
        "--title",
        default="BlockDoc: A Modern Approach to Structured Content",
        help="Article title",
    )
    parser.add_argument(
        "--topic",
        default="structured content formats for modern applications",
        help="Article topic",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update an existing article instead of creating a new one",
    )
    parser.add_argument("--input", help="Input JSON file (for update mode)")
    parser.add_argument("--block-id", help="Block ID to update (for update mode)")
    parser.add_argument("--instruction", help="Update instruction (for update mode)")
    parser.add_argument("--output-dir", default="./output", help="Output directory")

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    if args.update:
        # Update an existing document
        if not args.input or not args.block_id or not args.instruction:
            print("Error: update mode requires --input, --block-id, and --instruction")
            return

        print(f"Loading document from {args.input}...")
        with open(args.input, encoding="utf-8") as f:
            document = BlockDocDocument.from_json(f.read())

        print(f"Updating block {args.block_id}...")
        document = update_block_with_llm(document, args.block_id, args.instruction)

        # Save the updated document
        output_file = os.path.basename(args.input)
        updated_path = os.path.join(args.output_dir, f"updated_{output_file}")

        with open(updated_path, "w", encoding="utf-8") as f:
            f.write(document.to_json(indent=2))
        print(f"Updated document saved to {updated_path}")

        # Also save HTML for preview
        html_path = os.path.join(args.output_dir, f"updated_{os.path.splitext(output_file)[0]}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(document.render_to_html())
        print(f"HTML preview saved to {html_path}")

    else:
        # Create a new document
        print(f"Generating article: {args.title} about {args.topic}...")
        document = create_article_with_llm(args.title, args.topic)

        # Validate the document
        print("Validating document...")
        try:
            document.validate()
            print("✓ Document is valid")
        except ValueError as e:
            print(f"✗ Validation error: {e}")
            return

        # Create a slug from the title for filenames
        slug = args.title.lower().replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")

        # Save as JSON
        json_path = os.path.join(args.output_dir, f"{slug}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(document.to_json(indent=2))
        print(f"✓ Saved JSON to {json_path}")

        # Save as HTML
        html_path = os.path.join(args.output_dir, f"{slug}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{document.article["title"]}</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .blockdoc-title {{ margin-bottom: 1.5rem; }}
        .blockdoc-block {{ margin-bottom: 1.5rem; }}
        .blockdoc-image {{ max-width: 100%; height: auto; }}
        .blockdoc-caption {{ font-size: 0.9rem; color: #666; text-align: center; margin-top: 0.5rem; }}
        .blockdoc-pre {{ background-color: #f5f5f5; border-radius: 4px; padding: 1rem; overflow-x: auto; }}
        .blockdoc-code {{ font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 0.9rem; }}
        .blockdoc-quote {{ border-left: 4px solid #ccc; padding-left: 1rem; font-style: italic; margin: 0; }}
        .blockdoc-divider {{ border: 0; border-top: 1px solid #eee; margin: 2rem 0; }}
        .author-info {{ color: #666; font-size: 0.9rem; margin-bottom: 2rem; }}
    </style>
</head>
<body>
    <div class="author-info">
        Generated by BlockDoc LLM Assistant | {datetime.datetime.now().strftime("%Y-%m-%d")}
    </div>
    {document.render_to_html()}
</body>
</html>"""
            f.write(html)
        print(f"✓ Saved HTML to {html_path}")

        # Save as Markdown
        md_path = os.path.join(args.output_dir, f"{slug}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            frontmatter = f"""---
title: "{document.article["title"]}"
author: "BlockDoc LLM Assistant"
date: "{datetime.datetime.now().strftime("%Y-%m-%d")}"
topic: "{args.topic}"
generated: true
---

"""
            f.write(frontmatter + document.render_to_markdown())
        print(f"✓ Saved Markdown to {md_path}")

        print("\nArticle generation complete!")
        print(f"Files saved to {os.path.abspath(args.output_dir)}")
        print("\nTo update a specific block, run:")
        print(
            f'python llm_content_generator.py --update --input {json_path} --block-id BLOCK_ID --instruction "Your instruction"'
        )


if __name__ == "__main__":
    main()
