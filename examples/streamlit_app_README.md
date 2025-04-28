# BlockDoc Markdown Converter Web App

A simple Streamlit-based web interface for converting Markdown to BlockDoc format.

![Screenshot of the BlockDoc Markdown Converter](https://placeholder.com/blockdoc-converter-screenshot.png)

## Features

- Real-time Markdown to BlockDoc conversion
- Side-by-side view of input and output
- Document metadata support
- HTML preview of the rendered BlockDoc document
- JSON download functionality
- User-friendly interface with a responsive layout

## Installation

To run this app locally:

1. Clone the BlockDoc repository:
   ```bash
   git clone https://github.com/berrydev-ai/blockdoc-python.git
   cd blockdoc-python
   ```

2. Install BlockDoc and Streamlit:
   ```bash
   pip install -e .
   pip install streamlit
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run examples/streamlit_app.py
   ```

2. Open the provided URL in your browser (typically `http://localhost:8501`).

3. Enter your Markdown content in the left panel, add optional metadata, and click "Convert to BlockDoc".

4. The right panel will display the generated BlockDoc JSON. You can also:
   - Download the JSON file
   - View the HTML rendering of the document

## Use Cases

- Content editors who want to quickly convert Markdown to structured BlockDoc format
- Developers testing BlockDoc integration in their applications
- Educational tool for learning about the BlockDoc structure
- Quick conversion tool for preparing content for LLM integration

## Requirements

- Python 3.8+
- BlockDoc package
- Streamlit

## License

Same as the main BlockDoc project. See the LICENSE file in the project root.