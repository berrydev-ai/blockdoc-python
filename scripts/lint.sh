#!/bin/bash

# Run ruff linting checks
echo "Running Ruff linter..."
ruff check blockdoc tests examples

# Run ruff formatting
echo "Running Ruff formatter..."
ruff format blockdoc tests examples

# Check for mypy type errors
echo "Running mypy type checking..."
mypy blockdoc

echo "Done!"