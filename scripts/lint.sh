#!/bin/bash

# Run ruff linting checks
echo "Running Ruff linter..."
ruff check .

# Run ruff formatting
echo "Running Ruff formatter..."
ruff format .

# Check for mypy type errors
echo "Running mypy type checking..."
mypy blockdoc

echo "Done!"