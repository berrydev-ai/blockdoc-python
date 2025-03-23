# Contributing to BlockDoc

Thank you for your interest in contributing to BlockDoc! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Pull Request Process](#pull-request-process)
7. [Issue Reporting](#issue-reporting)
8. [Feature Requests](#feature-requests)
9. [Community Guidelines](#community-guidelines)

## Getting Started

Before contributing, please:

1. Familiarize yourself with the [BlockDoc documentation](docs/)
2. Check existing [issues](https://github.com/berrydev-ai/blockdoc-python/issues) to see if your issue/feature has been discussed
3. Check existing [pull requests](https://github.com/berrydev-ai/blockdoc-python/pulls) to avoid duplication

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/blockdoc-python.git
   cd blockdoc-python
   ```
3. Set up the development environment:
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```

## Code Style

BlockDoc follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) with a few customizations:

- Line length: 88 characters
- Use docstrings for all public modules, functions, classes, and methods
- Type hints are encouraged for all functions
- Ruff is used for linting and formatting (compatible with Black style)

To check and fix code style:

```bash
# Run linting
ruff check blockdoc tests

# Run formatting
ruff format blockdoc tests

# Or use the provided scripts
./scripts/lint.sh
./scripts/format.sh
```

## Testing

We use pytest for testing. All new features should include tests, and bug fixes should include regression tests.

To run tests:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=blockdoc

# Run a specific test file
pytest tests/core/test_block.py
```

### Test Guidelines

1. Test files should be named `test_*.py`
2. Test functions should start with `test_`
3. Each test should be focused and test one specific behavior
4. Use fixtures where appropriate
5. Mock external services

## Documentation

Good documentation is crucial for BlockDoc. All new features should include:

1. Docstrings for all public API elements
2. Updates to relevant documentation files in the `docs/` directory
3. Example usage where appropriate

For docstrings, we follow the [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings):

```python
def example_function(param1, param2):
    """Short description of function.
    
    Longer description with more details about behavior,
    edge cases, etc.
    
    Args:
        param1 (type): Description of param1.
        param2 (type): Description of param2.
        
    Returns:
        type: Description of return value.
        
    Raises:
        ExceptionType: When and why this exception is raised.
    """
    # Implementation
```

## Pull Request Process

1. **Fork & Branch**: Create a branch in your fork for your contribution
2. **Implementation**: Make your changes, following code style and including tests
3. **Documentation**: Update documentation as needed
4. **Pull Request**: Submit a PR with a clear description:
   - What problem does it solve?
   - How was it tested?
   - Any breaking changes?
5. **Code Review**: Respond to any feedback from maintainers
6. **CI**: Ensure all CI checks pass

### PR Title and Description Guidelines

- Use clear, descriptive titles
- Reference any related issues using GitHub keywords (e.g., "Fixes #123")
- Describe what changes were made and why

## Issue Reporting

When reporting issues, please:

1. Check existing issues to avoid duplicates
2. Use the issue templates when available
3. Include clear reproduction steps
4. Mention your environment (Python version, OS, BlockDoc version)
5. Include any error messages or stack traces

## Feature Requests

For feature requests:

1. Clearly describe the problem the feature would solve
2. Suggest an approach if you have one in mind
3. Indicate if you're willing to help implement it

## Community Guidelines

We strive to maintain a welcoming and inclusive community. Please:

- Be respectful and considerate of others
- Focus on constructive feedback
- Be open to different viewpoints and experiences
- Gracefully accept constructive criticism

## License

By contributing to BlockDoc, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

Thank you for contributing to BlockDoc!