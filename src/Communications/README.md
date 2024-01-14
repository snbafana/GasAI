# Communications Folder Documentation

This folder contains the implementations of various classes that handle chat communications within a network of actors in the application. The chat system is a bit convoluted but basically, the chat schema is a directed graph. Each node is a chat object. But, a chat object can either be a groupchat between agents and a decider agent, or a chatone object with one sub agent. Chat objects are also async generators for easy propogation through the system. The main components are as follows:

## Schema.py

The `Schema` class defined here represents the schema of a communication network, which consists of various nodes (instances of subclasses of `Node`) connected by directed edges signifying communication paths. It includes methods for adding and removing nodes/paths, auto-splitting messages for parallel processing, finding common nodes between paths, and visualizing the network structure with Matplotlib.

The `Schema` class is the central organizing structure that manages the flow of messages through the network, ensuring messages are processed through the appropriate nodes based on the communication paths set up within its graph.

## Chats.py

This file contains the `Chat` and `ChatOne` classes.

- `Chat`: A class representing a chat environment that facilitates chat interactions within the network. It handles asynchronous message processing, utilizing `Decider` agents to manage chat flows. The chat class can be used both for terminal-based interactions and as part of a full chat interface when integrated with Gradio for interactive user experiences.

- `ChatOne`: A subclass of `Chat` designed for one-shot interactions, where only a single message exchange between a user and an agent is expected. It is useful for simple queries or commands requiring only a single response.

## Node.py

This file provides the abstract base class `Node`, which serves as a template for creating different types of nodes within a communication network. Derived classes of `Node` are expected to implement the asynchronous generator method `get_node_completion_gen` for processing messages through the node.

