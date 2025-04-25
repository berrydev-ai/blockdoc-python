import os

from setuptools import find_packages, setup

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="blockdoc",
    version="1.1.0",
    author="Eric Berry",
    author_email="eric@berrydev.ai",
    description="A simple, powerful standard for structured content that works beautifully with LLMs, humans, and modern editors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/berrydev-ai/blockdoc-python",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "blockdoc": ["schema/*.json"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    install_requires=[
        "markdown>=3.3.0",
        "pygments>=2.10.0",
        "jsonschema>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "twine>=4.0.0",
        ],
    },
    keywords=[
        "content",
        "cms",
        "llm",
        "markdown",
        "structured-content",
        "editor",
        "blocks",
        "document",
        "ai",
    ],
)
