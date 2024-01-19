# Welcome to Graph Async Swarm AI (GAS AI) 

Currently, I have not setup the system as a python package. To play with the tools, git clone this repo and install the `requirements.txt` file into an environment of your choosing (`Conda`, `VirtualEnv`). Here is a conda example:

```shell
conda create --name gasai
conda activate gasai
pip install -r requirements.txt
```

Then, export your OPENAI API Key to environment variables with 

On Mac: 
```shell 
EXPORT OPENAI_API_KEY=".."
```

On Windows:
```shell
setx OPENAI_API_KEY="..."
```

Then, you should be all set to test out this code! Each folder's code has a respective readme which can help you learn more about the project. Please feel free to contribute. 

To test the code, you can run any of the examples like `networking-team.py` or `documentation-team.py` with the activated environment

---

# Project Overview

This project implements a complex software system designed to facilitate communication between autonomous agents which perform various tasks. These agents are modeled as nodes in a communication network and are capable of performing research, file operations, programming tasks, and other utility functions. The system is built using a mixture of Python object-oriented programming and integration with OpenAI's services.

## src Directory Structure

The `src` directory contains several Python files that define the behavior of different teams of agents, along with subdirectories for components of the system, which include:

- `Communications`: Contains the schema definition for the communication network.
- `Nodes`: Contains various node definitions including different specialized agents.
- `Tools`: Contains tools for the agents to utilize.

Each subdirectory has its own README.md with more details.

## Key Components

- `dev-team.py`: Defines a development team communication flow with roles such as Developer Agent, File Agent, Research Agent, and Assistant Agent.
- `documentation_team.py`: Specifies the documentation team responsible for generating comprehensive documentation from codebases.
- `multipurposeteam.py`: Represents a multipurpose team capable of handling various tasks including research, file operations, and networking aid.
- `networking-team.py`: Details a networking team responsible for information gathering, file writing, and networking/meeting support.
- `research-team.py`: Defines a research team that searches the web to pull information.

Each Python file integrates various components from the `Communications`, `Nodes`, and `Tools` subdirectories to set up a network of agents, each performing specific roles laid out in their respective scripts.

The purpose of this system is to define a network of intercommunicating agents that can simulate teamwork to achieve complex tasks. This model leverages the power of AI through OpenAI's models and plans to achieve a system capable of autonomous and dynamic problem-solving.

## Usage

The codebase represents the foundational components needed to build such an autonomous system. The agents are instantiated with their duties and are meant to communicate within a simulated network to achieve their respective goals. The agents call upon specialized tools and respond to instructions provided to them.

When running any of these scripts, the system initializes and the agents begin their operations as per the script's design. The `Schema` class is extensively used to manage the communication between the nodes.


---

If you are interested in contacting me, my email is `snbafana@gmail.com`


