"""
BlockDoc Document

Core class for creating, manipulating and rendering BlockDoc documents
"""

import json

import jsonschema

from blockdoc.core.block import Block
from blockdoc.renderers.html import render_to_html
from blockdoc.renderers.markdown import render_to_markdown
from blockdoc.schema.loader import schema


class BlockDocDocument:
    """
    Create a new BlockDoc document
    """

    def __init__(self, options):
        """
        Initialize a new BlockDoc document

        Args:
            options (dict): Document initialization options
                - title (str): Document title
                - metadata (dict, optional): Optional document metadata
                - blocks (list, optional): Initial blocks to add
        """
        title = options.get("title")
        metadata = options.get("metadata", {})
        blocks = options.get("blocks", [])

        if not title:
            raise ValueError("Document title is required")

        self.article = {
            "title": title,
            "metadata": metadata,
            "blocks": [],
        }

        # Add initial blocks if provided
        if blocks and isinstance(blocks, list):
            for block_data in blocks:
                self.add_block(block_data)

    def validate(self):
        """
        Validate the document against the BlockDoc schema

        Returns:
            bool: True if valid

        Raises:
            ValueError: If validation fails
        """
        try:
            jsonschema.validate(instance={"article": self.article}, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Invalid BlockDoc document: {str(e)}")

    def add_block(self, block_data):
        """
        Add a block to the document

        Args:
            block_data (dict or Block): Block data or Block instance

        Returns:
            Block: The created block

        Raises:
            ValueError: If block with the same ID already exists
        """
        # If it's already a Block instance, convert to dict
        if isinstance(block_data, Block):
            block_data = block_data.to_dict()

        # Check if ID already exists
        if self.get_block(block_data["id"]):
            raise ValueError(f"Block with ID '{block_data['id']}' already exists")

        block = Block(block_data)
        self.article["blocks"].append(block.to_dict())
        return block

    def insert_block(self, block_data, position):
        """
        Insert a block at a specific position

        Args:
            block_data (dict or Block): Block data or Block instance
            position (int): Position to insert at

        Returns:
            Block: The created block

        Raises:
            ValueError: If block with the same ID already exists
        """
        # If it's already a Block instance, convert to dict
        if isinstance(block_data, Block):
            block_data = block_data.to_dict()

        # Check if ID already exists
        if self.get_block(block_data["id"]):
            raise ValueError(f"Block with ID '{block_data['id']}' already exists")

        block = Block(block_data)
        self.article["blocks"].insert(position, block.to_dict())
        return block

    def get_block(self, id):
        """
        Get a block by ID

        Args:
            id (str): Block ID

        Returns:
            dict or None: The block or None if not found
        """
        for block in self.article["blocks"]:
            if block["id"] == id:
                return block
        return None

    def update_block(self, id, updates):
        """
        Update a block by ID

        Args:
            id (str): Block ID
            updates (dict): Properties to update

        Returns:
            dict: The updated block

        Raises:
            ValueError: If block with the ID doesn't exist
        """
        index = -1
        for i, block in enumerate(self.article["blocks"]):
            if block["id"] == id:
                index = i
                break

        if index == -1:
            raise ValueError(f"Block with ID '{id}' not found")

        # Create a new block with the updates
        current_block = self.article["blocks"][index]
        updated_data = {**current_block, **updates}

        # Validate the updated block
        block = Block(updated_data)

        # Update the block in the document
        self.article["blocks"][index] = block.to_dict()

        return self.article["blocks"][index]

    def remove_block(self, id):
        """
        Remove a block by ID

        Args:
            id (str): Block ID

        Returns:
            bool: True if removed, False if not found
        """
        index = -1
        for i, block in enumerate(self.article["blocks"]):
            if block["id"] == id:
                index = i
                break

        if index == -1:
            return False

        self.article["blocks"].pop(index)
        return True

    def move_block(self, id, new_position):
        """
        Move a block to a new position

        Args:
            id (str): Block ID
            new_position (int): New position

        Returns:
            bool: True if moved, False if not found

        Raises:
            ValueError: If new_position is invalid
        """
        index = -1
        for i, block in enumerate(self.article["blocks"]):
            if block["id"] == id:
                index = i
                break

        if index == -1:
            return False

        if new_position < 0 or new_position >= len(self.article["blocks"]):
            raise ValueError(f"Invalid position: {new_position}")

        # Remove the block from its current position
        block = self.article["blocks"].pop(index)

        # Insert it at the new position
        self.article["blocks"].insert(new_position, block)

        return True

    def render_to_html(self):
        """
        Render the document to HTML

        Returns:
            str: HTML representation
        """
        return render_to_html(self.article)

    def render_to_markdown(self):
        """
        Render the document to Markdown

        Returns:
            str: Markdown representation
        """
        return render_to_markdown(self.article)

    def to_dict(self):
        """
        Export the document as a dictionary

        Returns:
            dict: Document as dictionary
        """
        return {"article": self.article}

    def to_json(self, indent=2):
        """
        Export the document as a JSON string

        Args:
            indent (int, optional): JSON indentation level

        Returns:
            str: Document as JSON string
        """
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data):
        """
        Create a BlockDoc document from a dictionary

        Args:
            data (dict): Document data

        Returns:
            BlockDocDocument: New document instance

        Raises:
            ValueError: If data is invalid
        """
        if not data.get("article"):
            raise ValueError("Invalid BlockDoc document: missing article property")

        article = data["article"]

        return cls(
            {
                "title": article.get("title"),
                "metadata": article.get("metadata", {}),
                "blocks": article.get("blocks", []),
            }
        )

    @classmethod
    def from_json(cls, json_str):
        """
        Create a BlockDoc document from a JSON string

        Args:
            json_str (str): JSON string

        Returns:
            BlockDocDocument: New document instance

        Raises:
            ValueError: If JSON is invalid
        """
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")
