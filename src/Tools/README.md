# Tools Folder Documentation

The `Tools` folder contains Python code that serves as a set of tools for various tasks related to file operations, web scraping, and executing commands. These tools appear to be designed for use within a larger framework or system that utilizes asynchronous operations and schemas defined in an external `instructor` module.

## Files Overview

- `ToolForge.py`: Contains definitions of several tools, each class inheriting from `OpenAISchema` and providing an `async run()` method for the associated functionality.
- `ToolImporter.py`: Provides functionality to convert tools from a different tool ecosystem (presumably `langchain tools`) to the format used in this framework.
- `__init__.py`: Simplifies the import of the ToolForge and ToolImporter modules.
- `__pycache__`: A directory typically containing Python 3 bytecode compiled and cached files.

## ToolForge.py

This file defines several tools classes:

- `ExecuteCommand`: Executes a specified terminal command.
- `CreateDir`: Creates a directory based on the supplied folder name.
- `CreateFile`: Writes a file with given content to disk.
- `Program`: Combines multiple `CreateFile` instances to represent a complete program.
- `GetFilesInDirectory`: Lists all files within a specified directory.
- `OpenFile`: Opens and reads the content of a file.
- `SearchWeb`: Searches the web with a specified phrase and returns results.
- `CreateDirective`: Creates a directive based on provided goals and additional information.
- `SiteScraper`: Scrape all text content from a specified URL.

Additionally, utility functions such as `remove_non_utf8_characters` and `preprocess` are defined for text processing, and `search` and `scrape` functions for web searching and scraping tasks.

## ToolImporter.py

- This file provides the `ToolImporter` class with methods to convert and integrate external tools from `langchain` into the current codebase schema.
- Methods such as `from_langchain_tools`, `from_langchain_tool`, and `from_openai_schema` are used to convert and adapt different tool types and schemas into the current system.
- The file also offers utility functions like `dereference_schema` and `reference_schema` to manage JSON schema references.
