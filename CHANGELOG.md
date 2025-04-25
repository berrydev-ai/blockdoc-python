# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-04-25

### Added

- New `markdown_to_blockdoc` converter for transforming Markdown documents to BlockDoc format
- Comprehensive parser that handles all core Markdown elements:
  - Headings (ATX and Setext styles)
  - Paragraphs with proper line break handling
  - Lists (ordered and unordered)
  - Code blocks with language detection
  - Block quotes with attribution
  - Images with captions
  - Horizontal rules
- Semantic ID generation based on content
- Example implementation in `examples/markdown_conversion_example.py`
- Test suite for the converter functionality

## [1.0.1] - 2024-09-15

### Fixed

- Fixed pyproject.toml syntax error and installation method in CI

## [1.0.0] - 2024-09-01

### Added

- Initial release of BlockDoc
- Core Block and BlockDocDocument classes
- HTML and Markdown renderers
- JSON schema validation
- Basic utility functions