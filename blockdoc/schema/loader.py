"""
BlockDoc Schema Loader

Loads the JSON schema for BlockDoc validation
"""

import json
import os

# Get the schema file path
schema_path = os.path.join(os.path.dirname(__file__), "blockdoc.schema.json")

# Load schema
with open(schema_path) as schema_file:
    schema = json.load(schema_file)
