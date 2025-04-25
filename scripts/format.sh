#!/bin/bash

# Run ruff formatter on the codebase
echo "Running Ruff formatter..."
ruff format blockdoc tests examples

echo "Done!"