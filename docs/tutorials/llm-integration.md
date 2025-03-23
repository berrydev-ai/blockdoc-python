# Integrating BlockDoc with Language Models

This tutorial demonstrates how to effectively integrate BlockDoc with Language Model (LLM) APIs to create, update, and enhance structured content.

## Table of Contents

1. [Why BlockDoc is Ideal for LLMs](#why-blockdoc-is-ideal-for-llms)
2. [Setting Up LLM Integration](#setting-up-llm-integration)
3. [Creating Content with LLMs](#creating-content-with-llms)
4. [Updating Specific Blocks](#updating-specific-blocks)
5. [Enhancing Existing Content](#enhancing-existing-content)
6. [Translating Documents](#translating-documents)
7. [Designing Effective Prompts](#designing-effective-prompts)
8. [Advanced Integration Patterns](#advanced-integration-patterns)
9. [Performance and Cost Optimization](#performance-and-cost-optimization)

## Why BlockDoc is Ideal for LLMs

BlockDoc's structure offers significant advantages when working with LLMs:

1. **Targeted Updates**: Make precise requests to update specific blocks by ID
2. **Structured Output**: Get predictable, structured content rather than free-form text
3. **Semantic Context**: Blocks contain meaningful IDs that provide context for the LLM
4. **Granular Control**: Modularize content for more efficient token usage and more focused generation

## Setting Up LLM Integration

First, let's set up a basic integration with an LLM service. This example uses OpenAI's API, but the principles apply to any LLM API:

```python
import os
import json
from openai import OpenAI
from blockdoc import BlockDocDocument, Block

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Helper function for LLM interaction
def generate_text_with_llm(prompt, model="gpt-4", max_tokens=1000):
    """Generate text using an LLM model"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful content creation assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content
```

## Creating Content with LLMs

Let's use an LLM to generate a complete BlockDoc document:

```python
def create_document_with_llm(title, topic, num_sections=3):
    """Create a complete BlockDoc document using an LLM"""
    # 1. Generate the document structure with the LLM
    prompt = f"""
    Create a structured document about "{topic}" with {num_sections} main sections.
    For each section, provide:
    - A section heading title
    - One paragraph of introductory text
    - A list of 3-4 key points
    
    Format your response as JSON with the following structure:
    {{
        "sections": [
            {{
                "heading": "Section Title",
                "intro": "Introduction text...",
                "points": ["Point 1", "Point 2", "Point 3"]
            }}
        ]
    }}
    """
    
    response = generate_text_with_llm(prompt)
    
    # Parse the JSON response
    try:
        content_structure = json.loads(response)
    except json.JSONDecodeError:
        # Fallback: Try to extract JSON from the response using regex or other means
        import re
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            content_structure = json.loads(json_match.group(1))
        else:
            raise ValueError("Could not parse LLM response as JSON")
    
    # 2. Create the BlockDoc document
    doc = BlockDocDocument({
        "title": title,
        "metadata": {
            "author": "AI Assistant",
            "topic": topic,
            "generated": True
        }
    })
    
    # 3. Add an introduction block
    intro_prompt = f"Write a 2-3 sentence introduction for an article titled '{title}' about {topic}."
    intro_content = generate_text_with_llm(intro_prompt, max_tokens=200)
    doc.add_block(Block.text("introduction", intro_content))
    
    # 4. Add the sections from the structure
    for i, section in enumerate(content_structure["sections"]):
        section_id = f"section-{i+1}"
        heading_id = f"{section_id}-heading"
        intro_id = f"{section_id}-intro"
        list_id = f"{section_id}-points"
        
        # Add heading
        doc.add_block(Block.heading(heading_id, 2, section["heading"]))
        
        # Add intro paragraph
        doc.add_block(Block.text(intro_id, section["intro"]))
        
        # Add bullet points
        doc.add_block(Block.list(list_id, section["points"], "unordered"))
    
    # 5. Add a conclusion
    conclusion_prompt = f"Write a brief conclusion for an article about {topic}."
    conclusion_content = generate_text_with_llm(conclusion_prompt, max_tokens=200)
    doc.add_block(Block.text("conclusion", conclusion_content))
    
    return doc

# Usage example
document = create_document_with_llm(
    "BlockDoc: Structured Content for the AI Age",
    "how structured content formats enhance AI content generation"
)

# Save the document
with open("generated_article.json", "w") as f:
    f.write(document.to_json(indent=2))

# Render to HTML
with open("generated_article.html", "w") as f:
    f.write(document.render_to_html())
```

## Updating Specific Blocks

One of BlockDoc's strengths is the ability to target specific blocks for updates:

```python
async def update_block_with_llm(document, block_id, instruction):
    """Update a specific block in a document using an LLM"""
    # 1. Get the existing block
    block = document.get_block(block_id)
    if not block:
        raise ValueError(f"Block with ID '{block_id}' not found")
    
    # 2. Create a prompt based on the block type
    block_type = block["type"]
    content = block.get("content", "")
    
    if block_type == "text":
        prompt = f"""
        Here is an existing text block:
        
        {content}
        
        Please update this text according to this instruction: {instruction}
        
        Preserve any markdown formatting as appropriate. Return only the updated text.
        """
    elif block_type == "heading":
        prompt = f"""
        Here is an existing heading:
        
        {content}
        
        Please update this heading according to this instruction: {instruction}
        
        Keep it concise and clear. Return only the updated heading text.
        """
    elif block_type == "list":
        items = block.get("items", [])
        items_text = "\n".join([f"- {item}" for item in items])
        
        prompt = f"""
        Here is an existing list:
        
        {items_text}
        
        Please update this list according to this instruction: {instruction}
        
        Format your response as a JSON array of strings, like this:
        ["Item 1", "Item 2", "Item 3"]
        """
    else:
        prompt = f"""
        Here is existing content of type {block_type}:
        
        {content}
        
        Please update this content according to this instruction: {instruction}
        
        Return only the updated content.
        """
    
    # 3. Generate the updated content
    updated_content = generate_text_with_llm(prompt)
    
    # 4. Process the response based on block type
    updates = {}
    
    if block_type == "list":
        try:
            # Try to parse JSON array
            updated_items = json.loads(updated_content)
            if isinstance(updated_items, list):
                updates["items"] = updated_items
            else:
                # Fallback: Extract items line by line
                updates["items"] = [line.strip().lstrip('-').strip() 
                                  for line in updated_content.split('\n') 
                                  if line.strip()]
        except json.JSONDecodeError:
            # Fallback: Extract items line by line
            updates["items"] = [line.strip().lstrip('-').strip() 
                              for line in updated_content.split('\n') 
                              if line.strip()]
    else:
        updates["content"] = updated_content
    
    # 5. Update the block
    document.update_block(block_id, updates)
    
    return document

# Usage example
document = BlockDocDocument.from_json(open("blog_post.json").read())

# Update a specific block
document = update_block_with_llm(
    document,
    "introduction",
    "Make the introduction more engaging and add a statistic about content creation."
)

# Update another block
document = update_block_with_llm(
    document,
    "section-2-points",
    "Add two more benefits related to SEO and content reusability."
)
```

## Enhancing Existing Content

You can use LLMs to enhance your BlockDoc content in various ways:

```python
def enhance_document_with_llm(document):
    """Enhance an existing document by adding details, citations, etc."""
    
    # 1. Get all text blocks for enhancement
    text_blocks = [(i, block) for i, block in enumerate(document.article["blocks"]) 
                  if block["type"] == "text"]
    
    for index, block in text_blocks:
        # Only enhance blocks that are short or lack detail
        if len(block["content"]) < 300:
            prompt = f"""
            Here is a text block that needs enhancement:
            
            {block["content"]}
            
            Please enhance this content by:
            1. Adding more specific details
            2. Ensuring it has a clear topic sentence and conclusion
            3. Making the language more engaging
            4. Preserving all existing information
            
            Return only the enhanced text.
            """
            
            enhanced_content = generate_text_with_llm(prompt)
            document.update_block(block["id"], {"content": enhanced_content})
    
    # 2. Add citations to factual claims if needed
    for index, block in enumerate(document.article["blocks"]):
        if block["type"] == "text" and any(keyword in block["content"].lower() 
                                         for keyword in ["according to", "research", "study", "found", "data"]):
            
            prompt = f"""
            This text appears to contain factual claims:
            
            {block["content"]}
            
            For each factual claim, please suggest a suitable citation or source in [Author, Year] format.
            Return a JSON object like this:
            {{
              "factual_claims": [
                {{
                  "claim": "the text of the claim",
                  "citation": "[Author, Year]"
                }}
              ]
            }}
            """
            
            citation_suggestions = generate_text_with_llm(prompt)
            
            # Parse the response (this would need more robust parsing in production)
            try:
                citation_data = json.loads(citation_suggestions)
                # Store the citations as a custom property on the block
                document.update_block(block["id"], {"citation_info": citation_data})
            except:
                # Fallback: Store the raw suggestion
                document.update_block(block["id"], {"citation_suggestions": citation_suggestions})
    
    return document
```

## Translating Documents

BlockDoc's structure makes it easy to translate content while preserving the overall structure:

```python
def translate_document(document, target_language):
    """Translate a BlockDoc document to another language"""
    
    # First, create a new document for the translation
    translated_doc = BlockDocDocument({
        "title": document.article["title"],  # We'll translate this later
        "metadata": document.article["metadata"].copy()
    })
    
    # Update the metadata to indicate this is a translation
    translated_doc.article["metadata"]["original_language"] = "en"
    translated_doc.article["metadata"]["language"] = target_language
    
    # Translate the title
    title_prompt = f"""
    Translate this title to {target_language}:
    
    {document.article["title"]}
    
    Return only the translated title.
    """
    translated_title = generate_text_with_llm(title_prompt, max_tokens=100)
    translated_doc.article["title"] = translated_title
    
    # Translate each block
    for block in document.article["blocks"]:
        block_id = block["id"]
        block_type = block["type"]
        
        # Create a new block with the same ID and type
        new_block = {"id": block_id, "type": block_type}
        
        # Translate based on block type
        if block_type == "text" or block_type == "heading":
            content_prompt = f"""
            Translate this {block_type} to {target_language}:
            
            {block["content"]}
            
            Preserve any markdown formatting. Return only the translated text.
            """
            new_block["content"] = generate_text_with_llm(content_prompt)
            
            # Copy any other properties
            for key, value in block.items():
                if key not in ["id", "type", "content"]:
                    new_block[key] = value
        
        elif block_type == "list":
            items = block.get("items", [])
            items_text = "\n".join([f"- {item}" for item in items])
            
            items_prompt = f"""
            Translate this list to {target_language}:
            
            {items_text}
            
            Format your response as a JSON array of strings, like this:
            ["Translated Item 1", "Translated Item 2", "Translated Item 3"]
            """
            
            response = generate_text_with_llm(items_prompt)
            
            try:
                translated_items = json.loads(response)
                new_block["items"] = translated_items
            except:
                # Fallback: Extract translated items line by line
                new_block["items"] = [line.strip().lstrip('-').strip() 
                                    for line in response.split('\n') 
                                    if line.strip()]
            
            # Copy the list type and other properties
            new_block["list_type"] = block.get("list_type", block.get("listType", "unordered"))
            new_block["content"] = ""  # Lists typically have empty content
        
        elif block_type == "image" or block_type == "embed":
            # For media blocks, only translate captions and alt text
            new_block = block.copy()  # Copy all properties
            
            if "alt" in block:
                alt_prompt = f"""
                Translate this image alternative text to {target_language}:
                
                {block["alt"]}
                
                Return only the translated text.
                """
                new_block["alt"] = generate_text_with_llm(alt_prompt, max_tokens=100)
            
            if "caption" in block:
                caption_prompt = f"""
                Translate this caption to {target_language}:
                
                {block["caption"]}
                
                Return only the translated text.
                """
                new_block["caption"] = generate_text_with_llm(caption_prompt, max_tokens=100)
        
        elif block_type == "divider":
            # Dividers don't need translation
            new_block = block.copy()
        
        # Add the translated block to the document
        translated_doc.add_block(new_block)
    
    return translated_doc
```

## Designing Effective Prompts

When working with LLMs and BlockDoc, effective prompts are crucial for getting the desired output:

### Template for Block Creation

```python
def create_block_prompt(block_type, context, instructions):
    """Generate a prompt for creating a specific block type"""
    
    base_prompt = f"""
    You are generating content for a {block_type} block in a structured document.
    
    Context information:
    {context}
    
    Instructions:
    {instructions}
    """
    
    if block_type == "text":
        return base_prompt + """
        Create a well-formatted paragraph using Markdown for emphasis where appropriate.
        Return only the content text, without any explanations or metadata.
        """
    
    elif block_type == "heading":
        return base_prompt + """
        Create a concise, clear heading.
        Return only the heading text, without any formatting or punctuation at the end.
        """
    
    elif block_type == "list":
        return base_prompt + """
        Create a list of items.
        Format your response as a JSON array of strings, like this:
        ["Item 1", "Item 2", "Item 3"]
        
        Each item should be concise and clear, with Markdown formatting if needed.
        """
    
    # Add more block types as needed
    
    return base_prompt

# Example usage
heading_prompt = create_block_prompt(
    "heading",
    "This is for a section about BlockDoc's advantages for LLM integration",
    "Create a heading that emphasizes the efficiency gains from using BlockDoc with LLMs"
)
heading_content = generate_text_with_llm(heading_prompt, max_tokens=50)
```

### Prompt Engineering Tips

1. **Be specific about the format**: For lists and structured data, request JSON format
2. **Provide context**: Include surrounding blocks for context when updating 
3. **Set clear boundaries**: Ask for only the content, not explanations or metadata
4. **Use examples**: Show examples of desired output format for complex blocks
5. **Control verbosity**: Set appropriate max_tokens values for different block types

## Advanced Integration Patterns

Here are some advanced patterns for integrating BlockDoc with LLMs:

### Content Plans with LLMs

```python
def create_content_plan(topic, target_audience, content_type="blog"):
    """Use an LLM to create a content plan before generating the full document"""
    
    planning_prompt = f"""
    Create a detailed content plan for a {content_type} about "{topic}" targeted at {target_audience}.
    
    Your plan should include:
    1. A compelling title
    2. A brief summary of the content (2-3 sentences)
    3. 4-6 main sections with titles
    4. For each section, list 2-3 key points to cover
    5. Types of media to include (images, code examples, etc.)
    6. A call to action for the conclusion
    
    Format your response as JSON:
    {{
      "title": "The title",
      "summary": "Brief summary...",
      "sections": [
        {{
          "title": "Section title",
          "key_points": ["Point 1", "Point 2"],
          "media": ["Image showing X", "Code example of Y"]
        }}
      ],
      "call_to_action": "What the reader should do next"
    }}
    """
    
    response = generate_text_with_llm(planning_prompt, max_tokens=1500)
    
    try:
        # Parse the content plan
        content_plan = json.loads(response)
        
        # Create a BlockDoc document from the plan
        doc = BlockDocDocument({
            "title": content_plan["title"],
            "metadata": {
                "summary": content_plan["summary"],
                "topic": topic,
                "audience": target_audience,
                "content_type": content_type
            }
        })
        
        # Add introduction
        intro_prompt = f"""
        Write an engaging introduction for an article titled "{content_plan["title"]}" about {topic}.
        The audience is {target_audience}.
        The introduction should be 2-3 paragraphs and should include these key points:
        - What the article is about
        - Why it matters to the reader
        - What they'll learn
        
        Use Markdown for formatting. Return only the introduction text.
        """
        intro_content = generate_text_with_llm(intro_prompt, max_tokens=500)
        doc.add_block(Block.text("introduction", intro_content))
        
        # Process each section
        for i, section in enumerate(content_plan["sections"]):
            section_id = f"section-{i+1}"
            
            # Add section heading
            doc.add_block(Block.heading(
                f"{section_id}-heading",
                2,
                section["title"]
            ))
            
            # Create section content based on key points
            points_text = "\n".join([f"- {point}" for point in section["key_points"]])
            content_prompt = f"""
            Write a detailed section for an article about {topic} targeted at {target_audience}.
            
            Section title: {section["title"]}
            
            Include information about these key points:
            {points_text}
            
            The content should be 2-3 paragraphs with Markdown formatting.
            Return only the section content.
            """
            
            section_content = generate_text_with_llm(content_prompt, max_tokens=800)
            doc.add_block(Block.text(f"{section_id}-content", section_content))
            
            # Add media blocks if specified
            if "media" in section and section["media"]:
                for j, media_desc in enumerate(section["media"]):
                    if "code" in media_desc.lower():
                        # Add a code block
                        code_prompt = f"""
                        Create a code example for the section "{section["title"]}" about {topic}.
                        
                        Description: {media_desc}
                        
                        Return only the code, no explanations. 
                        Include comments to explain key parts of the code.
                        """
                        
                        code_content = generate_text_with_llm(code_prompt, max_tokens=500)
                        
                        # Determine the language from the description
                        language = "python"  # Default
                        for lang in ["python", "javascript", "html", "css", "java", "ruby", "php"]:
                            if lang in media_desc.lower():
                                language = lang
                                break
                        
                        doc.add_block(Block.code(
                            f"{section_id}-code-{j+1}",
                            language,
                            code_content
                        ))
                    
                    elif "image" in media_desc.lower():
                        # For images, we'd need a real source, but here we'll just create a placeholder
                        doc.add_block(Block.image(
                            f"{section_id}-image-{j+1}",
                            "https://placehold.co/600x400?text=Image+placeholder",
                            media_desc,
                            f"Figure: {media_desc}"
                        ))
        
        # Add conclusion with call to action
        conclusion_prompt = f"""
        Write a conclusion for an article titled "{content_plan["title"]}" about {topic}.
        
        Include this call to action: {content_plan["call_to_action"]}
        
        The conclusion should summarize the key points and motivate the reader to take action.
        Use Markdown for formatting. Return only the conclusion text.
        """
        
        conclusion_content = generate_text_with_llm(conclusion_prompt, max_tokens=400)
        doc.add_block(Block.text("conclusion", conclusion_content))
        
        return doc
        
    except json.JSONDecodeError:
        # Handle parsing errors
        raise ValueError("Could not parse LLM response as JSON")
```

### Review and Improve Content

```python
def review_and_improve_document(document):
    """Use an LLM to review and suggest improvements for a document"""
    
    # First, gather statistics about the document
    block_count = len(document.article["blocks"])
    block_types = {}
    word_count = 0
    
    for block in document.article["blocks"]:
        block_type = block["type"]
        block_types[block_type] = block_types.get(block_type, 0) + 1
        
        if block_type == "text":
            # Count words in text blocks
            word_count += len(block["content"].split())
    
    # Create a document summary
    doc_summary = f"""
    Document Title: {document.article["title"]}
    Block Count: {block_count}
    Word Count: {word_count}
    Block Types: {', '.join([f"{k}: {v}" for k, v in block_types.items()])}
    """
    
    # Review prompt
    review_prompt = f"""
    You are a content editor reviewing a structured document. Here's a summary of the document:
    
    {doc_summary}
    
    Please analyze the document's structure and content to identify areas for improvement:
    
    1. Does the document have a logical structure?
    2. Are there any sections that seem underdeveloped?
    3. Is there a good balance of block types?
    4. Are there opportunities to add media or interactive elements?
    5. Is the document's length appropriate for its purpose?
    
    Format your response as JSON:
    {{
      "overall_assessment": "Brief assessment of the document",
      "strengths": ["Strength 1", "Strength 2"],
      "areas_for_improvement": [
        {{
          "issue": "Description of the issue",
          "suggestion": "Specific suggestion for improvement",
          "priority": "high/medium/low"
        }}
      ],
      "recommended_additions": [
        {{
          "block_type": "text/image/list/etc.",
          "location": "Where to add it (after which existing block)",
          "description": "What this block should contain"
        }}
      ]
    }}
    """
    
    response = generate_text_with_llm(review_prompt, max_tokens=1000)
    
    try:
        review_data = json.loads(response)
        
        # Store the review as document metadata
        document.article["metadata"]["review"] = review_data
        
        # Implement high-priority improvements automatically
        for improvement in review_data.get("areas_for_improvement", []):
            if improvement.get("priority") == "high":
                # Find relevant blocks to improve based on issue description
                # This would need more sophisticated matching in a real system
                issue = improvement["issue"].lower()
                
                for block in document.article["blocks"]:
                    if block["type"] == "text" and any(keyword in block["content"].lower() 
                                                    for keyword in issue.split()):
                        
                        improve_prompt = f"""
                        Improve this text block based on this feedback:
                        
                        Issue: {improvement["issue"]}
                        Suggestion: {improvement["suggestion"]}
                        
                        Original content:
                        {block["content"]}
                        
                        Return only the improved content.
                        """
                        
                        improved_content = generate_text_with_llm(improve_prompt)
                        document.update_block(block["id"], {"content": improved_content})
                        
                        # Mark this improvement as applied
                        improvement["applied"] = True
                        break
        
        # Add recommended blocks
        for addition in review_data.get("recommended_additions", []):
            block_type = addition.get("block_type")
            location = addition.get("location")
            description = addition.get("description")
            
            # Find the position to insert the new block
            position = 0
            if location:
                for i, block in enumerate(document.article["blocks"]):
                    if location.lower() in block["id"].lower():
                        position = i + 1
                        break
            
            # Generate content for the new block
            if block_type == "text":
                content_prompt = f"""
                Create a text block with this description:
                {description}
                
                It should flow well with the surrounding content in the document.
                Use Markdown formatting as appropriate. Return only the content.
                """
                
                content = generate_text_with_llm(content_prompt)
                new_block = Block.text(f"added-text-{position}", content)
                
            elif block_type == "list":
                list_prompt = f"""
                Create a list with this description:
                {description}
                
                Format your response as a JSON array of strings.
                Each item should be concise and informative.
                """
                
                response = generate_text_with_llm(list_prompt)
                try:
                    items = json.loads(response)
                    new_block = Block.list(f"added-list-{position}", items, "unordered")
                except:
                    # Fallback
                    items = [line.strip().lstrip('-').strip() 
                            for line in response.split('\n') 
                            if line.strip()]
                    new_block = Block.list(f"added-list-{position}", items, "unordered")
                    
            elif block_type == "heading":
                heading_prompt = f"""
                Create a heading with this description:
                {description}
                
                It should be concise and descriptive.
                Return only the heading text.
                """
                
                content = generate_text_with_llm(heading_prompt, max_tokens=50)
                new_block = Block.heading(f"added-heading-{position}", 2, content)
            
            # Add more block types as needed
            
            # Insert the new block
            document.insert_block(new_block, position)
            
            # Mark this addition as applied
            addition["applied"] = True
        
        return document
        
    except json.JSONDecodeError:
        # Handle parsing errors
        raise ValueError("Could not parse LLM response as JSON")
```

## Performance and Cost Optimization

When working with LLMs and BlockDoc, consider these strategies to optimize performance and costs:

### Batching Related Operations

```python
def batch_generate_sections(document, section_ids, instructions):
    """Generate multiple sections in a single LLM call to reduce API calls"""
    
    sections_prompt = """
    Generate content for multiple sections of a document simultaneously.
    For each section, I'll provide the section ID, its purpose, and specific instructions.
    
    Format your response as JSON with this structure:
    {
      "sections": [
        {
          "id": "section-1",
          "content": "The generated content for section 1..."
        },
        {
          "id": "section-2",
          "content": "The generated content for section 2..."
        }
      ]
    }
    
    Here are the sections to generate:
    """
    
    for i, section_id in enumerate(section_ids):
        sections_prompt += f"""
        SECTION {i+1}:
        ID: {section_id}
        Instructions: {instructions[i]}
        
        """
    
    response = generate_text_with_llm(sections_prompt, max_tokens=2000)
    
    try:
        sections_data = json.loads(response)
        
        # Update each section in the document
        for section in sections_data["sections"]:
            document.update_block(section["id"], {"content": section["content"]})
        
        return document
        
    except json.JSONDecodeError:
        # Handle parsing errors
        raise ValueError("Could not parse LLM response as JSON")
```

### Caching Strategies

```python
import hashlib
import os
import json
import time

class SimpleLLMCache:
    """Simple cache for LLM responses to avoid duplicate API calls"""
    
    def __init__(self, cache_dir="./llm_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, prompt, model):
        """Generate a unique cache key for a prompt and model"""
        # Create a hash of the prompt and model
        hash_input = f"{prompt}|{model}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key):
        """Get the file path for a cache key"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, prompt, model):
        """Get a cached response if available"""
        cache_key = self._get_cache_key(prompt, model)
        cache_path = self._get_cache_path(cache_key)
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    cache_data = json.load(f)
                
                # Check if cache is expired (default: 24 hours)
                cache_time = cache_data.get("timestamp", 0)
                if time.time() - cache_time < 86400:  # 24 hours
                    return cache_data.get("response")
            except:
                pass
        
        return None
    
    def set(self, prompt, model, response):
        """Cache a response"""
        cache_key = self._get_cache_key(prompt, model)
        cache_path = self._get_cache_path(cache_key)
        
        cache_data = {
            "timestamp": time.time(),
            "prompt": prompt,
            "model": model,
            "response": response
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f)

# Use the cache with the generate function
cache = SimpleLLMCache()

def cached_generate_text_with_llm(prompt, model="gpt-4", max_tokens=1000):
    """Generate text using an LLM with caching"""
    # Check cache first
    cached_response = cache.get(prompt, model)
    if cached_response:
        return cached_response
    
    # Generate new response if not in cache
    response = generate_text_with_llm(prompt, model, max_tokens)
    
    # Cache the response
    cache.set(prompt, model, response)
    
    return response
```

### Using Smaller Models for Simple Tasks

```python
def generate_with_appropriate_model(prompt, task_complexity="medium"):
    """Choose an appropriate model based on task complexity"""
    
    if task_complexity == "low":
        # Use a smaller, faster model for simple tasks
        model = "gpt-3.5-turbo"
        max_tokens = 300
    elif task_complexity == "medium":
        # Default model for most tasks
        model = "gpt-4"
        max_tokens = 800
    else:  # high complexity
        # Use the most capable model for complex tasks
        model = "gpt-4"
        max_tokens = 2000
    
    return generate_text_with_llm(prompt, model, max_tokens)

# Task-specific wrappers
def generate_block_title(description):
    """Generate a simple block title (low complexity)"""
    prompt = f"Create a concise, clear title for a section about: {description}"
    return generate_with_appropriate_model(prompt, "low")

def generate_detailed_explanation(topic, context):
    """Generate a detailed explanation (high complexity)"""
    prompt = f"""
    Create a comprehensive explanation about {topic}.
    
    Context:
    {context}
    
    Include technical details, examples, and consider different perspectives.
    """
    return generate_with_appropriate_model(prompt, "high")
```

## Conclusion

BlockDoc's structured approach to content makes it an ideal format for LLM integration. By using the techniques in this tutorial, you can create powerful, efficient workflows that leverage the strengths of both BlockDoc and language models.

By breaking content into semantic blocks, you gain precise control over content generation, can target updates to specific sections, and maintain a clean, structured document that works beautifully with both human and AI authors.

For more examples of BlockDoc and LLM integration, check out the [LLM Integration Examples](../../examples/llm-integration/) directory.