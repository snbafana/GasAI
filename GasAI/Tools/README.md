# Tools

The `Tools` directory contains modules that provide specialized functionalities to the agents within the network. These tools are callable as methods and contribute to the tasks the agents can perform.

## Components

- `ToolForge.py`: Includes implementations of tools that can be employed by agents to perform actions like web searches, command executions, file operations, directory management, and more, powered largely through function calls.
- `ToolImporter.py`: Handles the importing of external tool definitions to be used by the agents in the system.
- `webtools.py`: Defines additional web-based tools for agents such as a Google search tool and a LinkedIn profile searcher.

Tools provided in this directory are integral to the operation and effectiveness of the agents in the network. They allow agents to perform complex tasks by interfacing with various services, accessing file systems, and scraping web data as needed.
