"""
BlockDoc Block

Represents a single content block within a BlockDoc document
"""

# Define allowed block types
ALLOWED_TYPES = [
    "text",
    "heading",
    "image",
    "code",
    "list",
    "quote",
    "embed",
    "divider",
]

# Define type-specific required properties
TYPE_REQUIREMENTS = {
    "heading": ["level"],
    "code": ["language"],
    "image": ["url", "alt"],
    "list": ["items", "list_type"],
}


class Block:
    """
    Create a new block
    """

    def __init__(self, data):
        """
        Initialize a new Block

        Args:
            data (dict): Block data
        """
        if not data.get("id"):
            raise ValueError("Block ID is required")

        if not data.get("type") or data.get("type") not in ALLOWED_TYPES:
            raise ValueError(f"Invalid block type: {data.get('type')}. Allowed types are: {', '.join(ALLOWED_TYPES)}")

        # Basic properties all blocks have
        self.id = data["id"]
        self.type = data["type"]
        self.content = data.get("content", "")

        # Check type-specific required properties
        required_props = TYPE_REQUIREMENTS.get(self.type, [])
        for prop in required_props:
            # Convert camelCase to snake_case for Python
            python_prop = prop
            if prop == "listType":
                python_prop = "list_type"

            if python_prop not in data and prop not in data:
                raise ValueError(f'Block of type "{self.type}" requires property "{prop}"')

            # Check both formats and prefer snake_case
            if python_prop in data:
                setattr(self, python_prop, data[python_prop])
            else:
                setattr(self, python_prop, data[prop])

        # Copy any additional properties
        for key, value in data.items():
            if key not in ["id", "type", "content"] and not hasattr(self, key):
                setattr(self, key, value)

    def update(self, updates):
        """
        Update block properties

        Args:
            updates (dict): Properties to update

        Returns:
            Block: Updated block instance
        """
        # Cannot change block type or ID
        updates_copy = updates.copy()
        updates_copy.pop("id", None)
        updates_copy.pop("type", None)

        # Apply updates
        for key, value in updates_copy.items():
            setattr(self, key, value)

        return self

    def to_dict(self):
        """
        Convert block to dictionary

        Returns:
            dict: Block as dictionary
        """
        result = {
            "id": self.id,
            "type": self.type,
            "content": self.content,
        }

        # Add type-specific properties
        for key, value in self.__dict__.items():
            if key not in ["id", "type", "content"]:
                result[key] = value

        return result

    # Factory methods for creating common block types

    @classmethod
    def text(cls, id, content):
        """
        Create a text block

        Args:
            id (str): Block ID
            content (str): Markdown content

        Returns:
            Block: New block instance
        """
        return cls(
            {
                "id": id,
                "type": "text",
                "content": content,
            }
        )

    @classmethod
    def heading(cls, id, level, content):
        """
        Create a heading block

        Args:
            id (str): Block ID
            level (int): Heading level (1-6)
            content (str): Heading text

        Returns:
            Block: New block instance
        """
        return cls(
            {
                "id": id,
                "type": "heading",
                "level": level,
                "content": content,
            }
        )

    @classmethod
    def image(cls, id, url, alt, caption=None):
        """
        Create an image block

        Args:
            id (str): Block ID
            url (str): Image URL
            alt (str): Alt text
            caption (str, optional): Optional caption

        Returns:
            Block: New block instance
        """
        data = {
            "id": id,
            "type": "image",
            "content": "",
            "url": url,
            "alt": alt,
        }

        if caption:
            data["caption"] = caption

        return cls(data)

    @classmethod
    def code(cls, id, language, content):
        """
        Create a code block

        Args:
            id (str): Block ID
            language (str): Programming language
            content (str): Code content

        Returns:
            Block: New block instance
        """
        return cls(
            {
                "id": id,
                "type": "code",
                "language": language,
                "content": content,
            }
        )

    @classmethod
    def list(cls, id, items, list_type="unordered"):
        """
        Create a list block

        Args:
            id (str): Block ID
            items (list): List items
            list_type (str, optional): List type (ordered or unordered)

        Returns:
            Block: New block instance
        """
        return cls(
            {
                "id": id,
                "type": "list",
                "content": "",
                "items": items,
                "list_type": list_type,
            }
        )

    @classmethod
    def quote(cls, id, content, attribution=None):
        """
        Create a quote block

        Args:
            id (str): Block ID
            content (str): Quote content
            attribution (str, optional): Source attribution

        Returns:
            Block: New block instance
        """
        data = {
            "id": id,
            "type": "quote",
            "content": content,
        }

        if attribution:
            data["attribution"] = attribution

        return cls(data)

    @classmethod
    def embed(cls, id, url, embed_type, caption=None):
        """
        Create an embed block

        Args:
            id (str): Block ID
            url (str): URL of embedded content
            embed_type (str): Type of embed (youtube, twitter, etc)
            caption (str, optional): Optional caption

        Returns:
            Block: New block instance
        """
        data = {
            "id": id,
            "type": "embed",
            "content": "",
            "url": url,
            "embed_type": embed_type,
        }

        if caption:
            data["caption"] = caption

        return cls(data)

    @classmethod
    def divider(cls, id):
        """
        Create a divider block

        Args:
            id (str): Block ID

        Returns:
            Block: New block instance
        """
        return cls(
            {
                "id": id,
                "type": "divider",
                "content": "",
            }
        )
