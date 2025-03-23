"""
BlockDoc

A simple, powerful standard for structured content that works beautifully with LLMs, humans, and modern editors.
"""

from blockdoc.core.block import Block
from blockdoc.core.document import BlockDocDocument
from blockdoc.renderers.html import render_to_html
from blockdoc.renderers.markdown import render_to_markdown
from blockdoc.schema.loader import schema

__version__ = '1.0.1'
