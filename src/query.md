Research and fill in the latex report below. Include all these components of the GAS Framework

### Components of GAS AI Framework

1. **Backend**
    - Contains the main application logic for GAS AI.
    - Hosts schema types for defining agents, nodes, and edges.
    - Includes utilities for creating and managing communication schemas.
    - JsonFiles directory hosts data files like `agent_lib.json` and `swarm_data.json` which are integral to the framework's operations.

2. **Communications**
    - Implements the schema for node communications within the framework.
    - Comprises classes such as `Schema`, `UtilityNode` (e.g., Splitters, Joiners), and definitions for node communication.
    - Core classes are foundational to enabling the communication logics within the framework.


The `Communications` directory contains modules that outline the network communication schema utilized across the system.

- `Schema.py`: Defines the `Schema` class, which constructs the graph structure representing a communication network using a directed graph model, facilitating various operations like adding nodes, paths, and processing messages asynchronously through the system.

- `__init__.py`: Allows the directory to be treated as a Python package so that its modules can be easily imported elsewhere in the project.

The `Schema` class enables the construction and management of the communication network by keeping track of nodes and their interconnections. It provides methods to add and remove nodes and communication paths, and it implements utilities for traversing and visualizing the network.


3. **Examples**
    - Contains a `context` file and several Python example files.
    - Python files illustrate the framework application for different team types: development, documentation, and research.
    - These can function as guides, sample implementations, or test cases.

4. **Nodes**
    - Defines various node types within the GAS AI network.
    - Includes Agent, User, and Utility Agents, as well as base node definitions and chat system implementations.
    - Nodes are the active elements that interact within the network, processing and exchanging information.

Each node functions as an async generator

5. **Tools**
    - Provides utilities that support the framework's functionality.
    - Tools for testing, importing additional tools, and web information retrieval.
    - These utilities enhance the capabilities of the agents within the framework.

### Architecture

The GAS AI framework is architected around a core set of directories that define the different capabilities and entities within the system. The system seems to be modular, with each directory encapsulating specific functionalities that work together to form a coherent application.

- Backend logic serves as the engine of the framework, where the main business logic resides.
- Communication schemas establish the protocols and methods through which nodes and agents interact.
- The nodes themselves represent the entities within the framework that perform actions and communicate.
- Tools directory suggests a plug-in or service-oriented architecture, allowing for extensibility and integration of external functionalities.

### Functionality

- The backend manages the framework's data structures and rules of interaction.
- Communication schemas allow for the structured exchange of information between the different entities in the network.
- Example cases provide demonstration and guidelines on how to deploy the framework for specific team configurations.
- Nodes perform a variety of roles within the network, from the execution of tasks to the mediating of interactions.
- Tools offer additional services that can be leveraged by the nodes, further extending the capabilities of the framework and its agents.

Each component plays a specific role within the GAS AI framework, contributing to the overall capability of the system to perform complex tasks and collaborations via an agent-based structure.


\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[colorinlistoftodos]{todonotes}
\usepackage[colorlinks=true, allcolors=blue]{hyperref}
\usepackage{indentfirst}
\usepackage[a4paper,top=3cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry} 
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{booktabs} % For better looking tables
\usepackage{float}


\titleclass{\subsubsubsection}{straight}[\subsection]

\newcounter{subsubsubsection}[subsubsection]
\renewcommand\thesubsubsubsection{\thesubsubsection.\arabic{subsubsubsection}}
\renewcommand\theparagraph{\thesubsubsubsection.\arabic{paragraph}} % optional; useful if paragraphs are to be numbered

\titleformat{\subsubsubsection}
  {\normalfont\normalsize\bfseries}{\thesubsubsubsection}{1em}{}
\titlespacing*{\subsubsubsection}
{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}

\title{GAS AI: A Graph-Based Asynchronous Framework for AI Agents Systems}
\author{Soham Bafana}
\begin{document}
\maketitle


\section*{Abstract}

\section{Introduction}

\textbf{LLM (like chat GPT) are super important right now}

\textbf{Multiagent systems have been around for decades}

\textbf{LLMs are important for agent systems and multiagent systems}

Large Language Models (LLMs) are becoming increasingly essential for tasks involving reasoning and the use of tools \cite{yaoReActSynergizingReasoning2023, xiRisePotentialLarge2023}. They play a critical role in the development of agents aimed at solving complex problems. Given the complexity of these tasks, an effective strategy to enhance agent capabilities is through the deployment of multi-agent systems. These systems foster cooperation and communication among agents. Recent studies highlight the benefits of multi-agent systems, including the encouragement of divergent thinking \cite{liangEncouragingDivergentThinking2023}, the improvement of reasoning accuracy \cite{duImprovingFactualityReasoning2023}, and the provision of validation mechanisms \cite{wuEmpiricalStudyChallenging2023}. In light of these advantages, an important question arises: How can we construct LLM applications that harness the potential of multi-agent systems to tackle complex challenges effectively?

\textbf{There are a lot of other multi agent approaches, what are some of them and what do they introduce to us?}

- Autogen
- Langchain
- Taskweaver

Accepting the notion of the conversable agent that can accept feedback, tool calling, function calling + more.  Establish what the norm is, what is the average framework looking like. Once I do this, then I can move on.

\textbf{What makes GAS AI so good, what is it built on?}

While there is a wide variety of multi-agent approaches (Appendix A), we present GAS AI (Graph Asynchronous Swarm, Artificial Intelligence), a graph based asynchronous multi-agent communication framework. GAS AI is built on the following concepts: 

\begin{enumerate}
    \item Graph Based Communication Schema 
    \item Agents as Asynchronous Generators
    \item Parallel Inference
\end{enumerate}

\section{GAS AI Framework}

\subsection{Graph Based Communication}
Graph based communication- Network X. treating agents as nodes in a complex paradigm, schema class and communication between nodes. Defining each instance of a completion request object as a node, and allowing for the user to create connections between those nodes. Then, the user can execute the schema. 

\subsection{Asynchronous AI Generators}



\subsubsection{Instructor}


Asynchronous - each agent as an async generator, agent class, node class + more

\subsection{Parallel Inference}

Asynchronous - each agent as an async generator, agent class, node class + more

\section{Applications}

\section{Discussion}


Work is still in early experimental stages, but it paves the way for numerous future directions and research opportunities. 



\section{ORCID}

Soham Bafana: \url{ https://orcid.org/0009-0005-3681-1088}
\bibliographystyle{	apa}    
\bibliography{refs}
\end{document}