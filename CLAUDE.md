# BlockDoc Project Information

## Development Commands

### Linting and Formatting

- Run linting: `./scripts/lint.sh` or `ruff check .`
- Run formatting: `./scripts/format.sh` or `ruff format .`
- Install dev dependencies: `pip install -e ".[dev]"`

### Testing

- Run tests: `pytest` or `pytest tests/`

## Code Style

This project uses ruff for code style enforcement with the following settings:
- Line length: 88 characters
- Use double quotes for strings
- Follow black-compatible formatting

## Project Structure

- `blockdoc/`: Main package source code
  - `core/`: Core functionality (Block and Document classes)
  - `renderers/`: HTML and Markdown renderers
  - `schema/`: JSON schema for BlockDoc
  - `utils/`: Utility functions
- `tests/`: Test suite
- `examples/`: Example applications
- `docs/`: Documentation