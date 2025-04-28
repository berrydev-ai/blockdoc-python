"""
BlockDoc Markdown Converter Web App

A Streamlit-based web interface for converting Markdown to BlockDoc format
"""

import json
import os
from datetime import datetime

import streamlit as st

try:
    # Try to import directly (for deployed environment)
    from blockdoc import markdown_to_blockdoc
except ImportError:
    # Local development fallback
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from blockdoc import markdown_to_blockdoc

# Sample markdown for demonstration
SAMPLE_MARKDOWN = """# Markdown to BlockDoc Conversion

This is a demonstration of converting **Markdown** content to BlockDoc format.

## Key Features

BlockDoc makes it easy to work with structured content:

- Maintains semantic structure
- Preserves formatting
- Creates meaningful block IDs

### Code Examples

```python
from blockdoc import markdown_to_blockdoc

# Convert markdown to BlockDoc
doc = markdown_to_blockdoc(markdown_text)

# Export as JSON
json_str = doc.to_json()
print(json_str)
```

> This is a blockquote example
> with multiple lines
> — Example Author
"""

# Page configuration
st.set_page_config(
    page_title="BlockDoc Markdown Converter",
    page_icon="📝",
    layout="wide",
)

# Header
st.title("BlockDoc Markdown Converter")
st.markdown(
    "Convert your Markdown documents to BlockDoc's structured JSON format. "
    "BlockDoc is a simple, powerful standard for structured content that works "
    "beautifully with LLMs, humans, and modern editors."
)

# Create two columns
col1, col2 = st.columns(2)

# Left column - Markdown input
with col1:
    # Optional metadata
    with st.expander("Document Metadata (Optional)"):
        doc_title = st.text_input("Document Title:", "")
        author = st.text_input("Author:", "")
        tags_input = st.text_input("Tags (comma separated):", "")
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

    st.header("Markdown Input")
    markdown_text = st.text_area(
        "Enter your Markdown here:",
        value=SAMPLE_MARKDOWN,
        height=400,
    )

# Convert button
convert_button = st.button("Convert to BlockDoc", type="primary")

# Right column - BlockDoc JSON output
with col2:
    st.header("BlockDoc JSON Output")

    if convert_button or "doc_json" in st.session_state:
        try:
            # Create metadata dictionary
            metadata = {}
            if author:
                metadata["author"] = author
            if tags:
                metadata["tags"] = tags
            metadata["convertedDate"] = datetime.now().isoformat()

            # Convert markdown to BlockDoc
            doc = markdown_to_blockdoc(
                markdown_text, title=doc_title if doc_title else "Untitled Document", metadata=metadata
            )

            # Validate the document
            doc.validate()

            # Convert to JSON and format
            doc_json = doc.to_json(indent=2)
            st.session_state.doc_json = doc_json

            # Display JSON with syntax highlighting
            st.json(json.loads(doc_json))

            # Download button
            st.download_button(
                label="Download JSON",
                data=doc_json,
                file_name="blockdoc_output.json",
                mime="application/json",
            )

            # Preview rendered output
            with st.expander("Preview HTML Rendering"):
                html_output = doc.render_to_html()
                st.components.v1.html(html_output, height=500, scrolling=True)

        except Exception as e:
            st.error(f"Error converting markdown: {str(e)}")
    else:
        st.info("Enter Markdown on the left side and click 'Convert to BlockDoc' to see the result.")

# Footer with instructions
st.markdown("---")
st.markdown("""
### How to use:
1. Paste your Markdown content in the left panel
2. Add optional metadata if desired
3. Click 'Convert to BlockDoc' to generate the structured JSON
4. You can download the JSON output or preview the HTML rendering

### Run this app locally:
```bash
pip install streamlit
cd blockdoc-python
streamlit run examples/streamlit_app.py
```
""")
