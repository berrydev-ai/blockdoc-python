"""
Tests for Block class
"""

import pytest

from blockdoc.core.block import ALLOWED_TYPES, Block


def test_block_init():
    """Test Block initialization with valid data"""
    # Test text block
    text_block = Block({"id": "intro", "type": "text", "content": "Hello world"})
    assert text_block.id == "intro"
    assert text_block.type == "text"
    assert text_block.content == "Hello world"

    # Test heading block
    heading_block = Block({"id": "title", "type": "heading", "level": 1, "content": "Title"})
    assert heading_block.id == "title"
    assert heading_block.type == "heading"
    assert heading_block.level == 1
    assert heading_block.content == "Title"


def test_block_init_missing_id():
    """Test Block initialization with missing ID"""
    with pytest.raises(ValueError) as excinfo:
        Block({"type": "text", "content": "Hello world"})
    assert "Block ID is required" in str(excinfo.value)


def test_block_init_invalid_type():
    """Test Block initialization with invalid type"""
    with pytest.raises(ValueError) as excinfo:
        Block({"id": "intro", "type": "invalid-type", "content": "Hello world"})
    assert "Invalid block type" in str(excinfo.value)
    assert "invalid-type" in str(excinfo.value)
    for allowed_type in ALLOWED_TYPES:
        assert allowed_type in str(excinfo.value)


def test_block_init_missing_required_props():
    """Test Block initialization with missing required properties for specific types"""
    # Heading without level
    with pytest.raises(ValueError) as excinfo:
        Block({"id": "title", "type": "heading", "content": "Title"})
    assert 'requires property "level"' in str(excinfo.value)

    # Code without language
    with pytest.raises(ValueError) as excinfo:
        Block({"id": "code", "type": "code", "content": "function() {}"})
    assert 'requires property "language"' in str(excinfo.value)

    # Image without url and alt
    with pytest.raises(ValueError) as excinfo:
        Block({"id": "image", "type": "image", "content": ""})
    assert "requires property" in str(excinfo.value) and ("url" in str(excinfo.value) or "alt" in str(excinfo.value))


def test_block_update():
    """Test Block.update method"""
    block = Block({"id": "intro", "type": "text", "content": "Hello world"})

    # Update content
    block.update({"content": "Updated content"})
    assert block.content == "Updated content"

    # Try to update id and type (should be ignored)
    block.update({"id": "new-id", "type": "heading", "content": "New content"})
    assert block.id == "intro"  # Unchanged
    assert block.type == "text"  # Unchanged
    assert block.content == "New content"  # Changed


def test_block_to_dict():
    """Test Block.to_dict method"""
    block_data = {"id": "intro", "type": "text", "content": "Hello world"}
    block = Block(block_data)

    # Convert to dict and verify
    result = block.to_dict()
    assert result == block_data


def test_block_factory_methods():
    """Test Block factory methods"""
    # Text block
    text_block = Block.text("intro", "Hello world")
    assert text_block.id == "intro"
    assert text_block.type == "text"
    assert text_block.content == "Hello world"

    # Heading block
    heading_block = Block.heading("title", 1, "Title")
    assert heading_block.id == "title"
    assert heading_block.type == "heading"
    assert heading_block.level == 1
    assert heading_block.content == "Title"

    # Image block
    image_block = Block.image("hero", "https://example.com/image.jpg", "Alt text", "Caption")
    assert image_block.id == "hero"
    assert image_block.type == "image"
    assert image_block.url == "https://example.com/image.jpg"
    assert image_block.alt == "Alt text"
    assert image_block.caption == "Caption"

    # Code block
    code_block = Block.code("snippet", "javascript", 'console.log("Hello");')
    assert code_block.id == "snippet"
    assert code_block.type == "code"
    assert code_block.language == "javascript"
    assert code_block.content == 'console.log("Hello");'

    # List block
    list_block = Block.list("items", ["Item 1", "Item 2"], "ordered")
    assert list_block.id == "items"
    assert list_block.type == "list"
    assert list_block.items == ["Item 1", "Item 2"]
    assert list_block.list_type == "ordered"

    # Quote block
    quote_block = Block.quote("quote", "Famous quote", "Famous person")
    assert quote_block.id == "quote"
    assert quote_block.type == "quote"
    assert quote_block.content == "Famous quote"
    assert quote_block.attribution == "Famous person"

    # Embed block
    embed_block = Block.embed("video", "https://youtube.com/watch?v=123", "youtube", "Video caption")
    assert embed_block.id == "video"
    assert embed_block.type == "embed"
    assert embed_block.url == "https://youtube.com/watch?v=123"
    assert embed_block.embed_type == "youtube"
    assert embed_block.caption == "Video caption"

    # Divider block
    divider_block = Block.divider("separator")
    assert divider_block.id == "separator"
    assert divider_block.type == "divider"
    assert divider_block.content == ""
