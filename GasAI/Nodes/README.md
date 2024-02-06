# Nodes

The `Nodes` directory contains files that define the structure and behavior of different types of agents and nodes in the network.

## Components

- `Agent.py`: Defines the `Agent` class that represents an actor within the system with specific functionality. It is responsible for managing the lifecycle of an agent including its creation, instruction-following, and interaction with OpenAI's API.
- `Chats.py`: Contains the `Chat` class which represents a chat environment, facilitating the interaction network of multiple actors or agents.
- `Node.py`: Establishes the base `Node` class from which other entities within the network inherit.
- `User.py`: Defines the `User` class, a specialized type of node within the network representing end-user interaction.
- `UtilityAgents.py`: Contains various utility agents such as `Splitter` and `Joiner` for managing task delegation and results consolidation in the network.

These components work in tandem to create a flexible and scalable network of agents, each capable of performing specific tasks set by their design. They use a combination of message passing, OpenAI API integration, and asynchronous operations to simulate a collaborative working environment.
