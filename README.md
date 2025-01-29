# Welcome to Graph Async Swarm AI (GAS AI) 

See the project demo here: https://youtu.be/VyzOhJB5668?si=iLsuFQalabbmkA8O

Currently, I have not setup the system as a python package. To play with the tools, git clone this repo and install the `requirements.txt` file into an environment of your choosing (`Conda`, `VirtualEnv`). Here is a conda example. Or, use the Test Colab provided. 

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

```python
from Communications import Schema
from Nodes import Developer, Assistant, User, SplitJoinPair
from Tools import SearchWebGOOGLE, CreateFile, GetFilesInDirectory, SiteScraper, LinkedINSearch

# Declare schema and 
comm:Schema = Schema()

swarm_goal = 'To answer to the users needs in all forms of information gathering, email and file writing, and networking/meeting aid'

# By defining the first node's communication schema, you define the entire system's schema
user = User(comm=comm)


# Create a research agent
research_node = Assistant(name='Research Agent', 
                        instructions=f"""You are the Research Agent, operating for the following swarm goal: {swarm_goal}
                                        You take in  queries/info and research the info through your function calling. 
                                        Return all the information you gained like links, web info, and most specifically website content. Function call concisely, as little as possible. 
                                        But you must do it. Cite all sources, and query with relevance. Do not ask for any advice. Just execute all the research you can do, navigate as many website, and return all your information""",
                        description="Responsible for searching the web and pulling information",
                        functions=[SearchWebGOOGLE, SiteScraper, LinkedINSearch])

# Create a file management agent
file_node = Assistant(name='File Agent', 
                        instructions=f"""You are the File Agent, operating for the following swarm goal: {swarm_goal} 
                        You take in information and links from the research agent, and write a markdown report that summarizes all that was learned. Some questions to think about are: 
                        If the user asks to write a report, follow their guidelines exactly. Do not deviate from the command, and for these reports on individuals, follow the following guidelines:
                        what is their authority, some important quotes or things they have done, and more. Prep the notes so that they are usable for a potential meeting
                        
                        You can read and write files""",
                    
                        description="responsbile for reading and writing files, most specifically, writing the report files",
                        functions=[CreateFile, GetFilesInDirectory],
                    )

# Create a splitter and joiner that are linked to one another
s, j = SplitJoinPair()

# Add the splitter and joiner so that the user's query will be split and handled simultaneously and this information will be combined and fed to the file node
user > s > research_node > j > file_node

# Run the communication schema
comm.startup(starting_node=user)

```


---

If you are interested in contacting me, my email is `snbafana@gmail.com`


