# Actors Folder Documentation

This folder defines the `Actor` entities of a messaging system, which encompasses different roles like users, agents, and utility agents. Each role is represented by a Python class that inherits from the `Actor` class, providing a framework for interaction within the system.

## Actor.py
This file contains the abstract base class `Actor`, which defines the basic interface for all actors within the system. The class uses Python's Abstract Base Class (ABC) module to define an abstract `send_message_gen` method, which encompasses the logic for sending messages asynchronously.

## Agent.py
Defines the `Agent` class which extends `Actor`, and is specifically designed for interacting with the OpenAI API. It also contains subclasses `Developer` and `Assistant` for specialized functionality. The `Agent` class is responsible for managing the lifecycle of agents, sending messages, and handling responses from the OpenAI API.

Each agent is an `Asyncronous Generator` that constantly yields new messages, function calls and more. Tools can be passed in as async functions, async generators, functions that return other functions, and more. 

## User.py
Contains the `User` class that represents a user in the system. It inherits from `Actor` and handles user-specific actions, such as sending messages. The user's responses can be input directly or read from a file.

## UtilityAgents.py
This file introduces utility classes that extend the `Agent` class to perform specialized functions:

- `Decider`: Manages the selection of agents for a given message based on achieving a specific goal.
- `Splitter`: Distributes a message among various recipient agents to achieve subgoals. When an agent task is split, I have not designed an easy way for three simultaneous tasks to be rejoined. Currently, if the goals are split over two agents, then those two agents can be pointed to a final agent which will take content from the finalized results of both agents. However, if goals are split over one path of agents, then the paths will not be rejoined. In this case, the line of agents would be duplicated, so there would be one "final" agent for each of the tasks. **I am still working this out, and need some help here**
- `Joiner`: Potentially collects outputs from multiple agents for recombination (not fully defined in the existing code). A joiner agent may be helpful. But currently, I do not have the user defining Splitter inputs and Joiner outputs. These are automatically created based on the user graph creation. In the future, it may be helpful to do this. 
- `GoalMaker`: Managing the establishment of goals (not fully defined)

