"""
Tests for BlockDocDocument class
"""

import json

import pytest

from blockdoc.core.block import Block
from blockdoc.core.document import BlockDocDocument


def test_document_init():
    """Test document initialization with valid data"""
    # Test with minimal options
    doc = BlockDocDocument({"title": "Test Document"})
    assert doc.article["title"] == "Test Document"
    assert doc.article["metadata"] == {}
    assert doc.article["blocks"] == []

    # Test with metadata
    doc = BlockDocDocument(
        {
            "title": "Test Document",
            "metadata": {"author": "Test Author", "tags": ["test", "document"]},
        }
    )
    assert doc.article["title"] == "Test Document"
    assert doc.article["metadata"]["author"] == "Test Author"
    assert doc.article["metadata"]["tags"] == ["test", "document"]

    # Test with initial blocks
    doc = BlockDocDocument(
        {
            "title": "Test Document",
            "blocks": [
                {"id": "intro", "type": "text", "content": "Introduction"},
                {"id": "heading", "type": "heading", "level": 2, "content": "Section"},
            ],
        }
    )
    assert len(doc.article["blocks"]) == 2
    assert doc.article["blocks"][0]["id"] == "intro"
    assert doc.article["blocks"][1]["id"] == "heading"


def test_document_init_missing_title():
    """Test document initialization with missing title"""
    with pytest.raises(ValueError) as excinfo:
        BlockDocDocument({})
    assert "Document title is required" in str(excinfo.value)


def test_document_add_block():
    """Test add_block method"""
    doc = BlockDocDocument({"title": "Test Document"})

    # Add a block
    block = doc.add_block({"id": "intro", "type": "text", "content": "Introduction"})

    assert isinstance(block, Block)
    assert len(doc.article["blocks"]) == 1
    assert doc.article["blocks"][0]["id"] == "intro"
    assert doc.article["blocks"][0]["type"] == "text"
    assert doc.article["blocks"][0]["content"] == "Introduction"

    # Add a Block instance
    heading_block = Block.heading("heading", 2, "Section")
    doc.add_block(heading_block)

    assert len(doc.article["blocks"]) == 2
    assert doc.article["blocks"][1]["id"] == "heading"
    assert doc.article["blocks"][1]["type"] == "heading"
    assert doc.article["blocks"][1]["level"] == 2

    # Try adding a block with existing ID
    with pytest.raises(ValueError) as excinfo:
        doc.add_block({"id": "intro", "type": "text", "content": "New introduction"})
    assert "Block with ID 'intro' already exists" in str(excinfo.value)


def test_document_insert_block():
    """Test insert_block method"""
    doc = BlockDocDocument({"title": "Test Document"})

    # Add some blocks
    doc.add_block(Block.text("intro", "Introduction"))
    doc.add_block(Block.text("conclusion", "Conclusion"))

    # Insert a block in the middle
    doc.insert_block(Block.heading("heading", 2, "Section"), 1)

    assert len(doc.article["blocks"]) == 3
    assert doc.article["blocks"][0]["id"] == "intro"
    assert doc.article["blocks"][1]["id"] == "heading"
    assert doc.article["blocks"][2]["id"] == "conclusion"


def test_document_get_block():
    """Test get_block method"""
    doc = BlockDocDocument({"title": "Test Document"})

    # Add a block
    doc.add_block(Block.text("intro", "Introduction"))

    # Get the block
    block = doc.get_block("intro")
    assert block is not None
    assert block["id"] == "intro"
    assert block["content"] == "Introduction"

    # Get a non-existent block
    block = doc.get_block("nonexistent")
    assert block is None


def test_document_update_block():
    """Test update_block method"""
    doc = BlockDocDocument({"title": "Test Document"})

    # Add a block
    doc.add_block(Block.text("intro", "Introduction"))

    # Update the block
    updated_block = doc.update_block("intro", {"content": "Updated introduction"})

    assert updated_block["content"] == "Updated introduction"
    assert doc.article["blocks"][0]["content"] == "Updated introduction"

    # Try to update a non-existent block
    with pytest.raises(ValueError) as excinfo:
        doc.update_block("nonexistent", {"content": "Content"})
    assert "Block with ID 'nonexistent' not found" in str(excinfo.value)


def test_document_remove_block():
    """Test remove_block method"""
    doc = BlockDocDocument({"title": "Test Document"})

    # Add blocks
    doc.add_block(Block.text("intro", "Introduction"))
    doc.add_block(Block.text("content", "Content"))

    # Remove a block
    result = doc.remove_block("intro")
    assert result is True
    assert len(doc.article["blocks"]) == 1
    assert doc.article["blocks"][0]["id"] == "content"

    # Try to remove a non-existent block
    result = doc.remove_block("nonexistent")
    assert result is False


def test_document_move_block():
    """Test move_block method"""
    doc = BlockDocDocument({"title": "Test Document"})

    # Add blocks
    doc.add_block(Block.text("intro", "Introduction"))
    doc.add_block(Block.text("content", "Content"))
    doc.add_block(Block.text("conclusion", "Conclusion"))

    # Move a block
    result = doc.move_block("conclusion", 0)
    assert result is True
    assert doc.article["blocks"][0]["id"] == "conclusion"
    assert doc.article["blocks"][1]["id"] == "intro"
    assert doc.article["blocks"][2]["id"] == "content"

    # Try to move a non-existent block
    result = doc.move_block("nonexistent", 0)
    assert result is False

    # Try to move to an invalid position
    with pytest.raises(ValueError) as excinfo:
        doc.move_block("intro", 10)
    assert "Invalid position" in str(excinfo.value)


def test_document_to_dict():
    """Test to_dict method"""
    doc = BlockDocDocument({"title": "Test Document", "metadata": {"author": "Test Author"}})

    doc.add_block(Block.text("intro", "Introduction"))

    # Convert to dict
    result = doc.to_dict()
    assert result["article"]["title"] == "Test Document"
    assert result["article"]["metadata"]["author"] == "Test Author"
    assert len(result["article"]["blocks"]) == 1
    assert result["article"]["blocks"][0]["id"] == "intro"


def test_document_to_json():
    """Test to_json method"""
    doc = BlockDocDocument({"title": "Test Document"})

    doc.add_block(Block.text("intro", "Introduction"))

    # Convert to JSON
    json_str = doc.to_json()
    data = json.loads(json_str)

    assert data["article"]["title"] == "Test Document"
    assert len(data["article"]["blocks"]) == 1
    assert data["article"]["blocks"][0]["id"] == "intro"


def test_document_from_dict():
    """Test from_dict method"""
    data = {
        "article": {
            "title": "Test Document",
            "metadata": {"author": "Test Author"},
            "blocks": [{"id": "intro", "type": "text", "content": "Introduction"}],
        }
    }

    # Create document from dict
    doc = BlockDocDocument.from_dict(data)

    assert doc.article["title"] == "Test Document"
    assert doc.article["metadata"]["author"] == "Test Author"
    assert len(doc.article["blocks"]) == 1
    assert doc.article["blocks"][0]["id"] == "intro"


def test_document_from_json():
    """Test from_json method"""
    json_str = json.dumps(
        {
            "article": {
                "title": "Test Document",
                "metadata": {"author": "Test Author"},
                "blocks": [{"id": "intro", "type": "text", "content": "Introduction"}],
            }
        }
    )

    # Create document from JSON
    doc = BlockDocDocument.from_json(json_str)

    assert doc.article["title"] == "Test Document"
    assert doc.article["metadata"]["author"] == "Test Author"
    assert len(doc.article["blocks"]) == 1
    assert doc.article["blocks"][0]["id"] == "intro"
