from abc import ABC, abstractmethod
from typing import List
from typing import AsyncGenerator
import os

class Node(ABC):
    """
    An abstract base class representing a node in a communication network.

    This class serves as a template for creating different types of nodes in a network.
    Each node can contain multiple actors and has a specific purpose within the network.

    Attributes:
        actors (list[Actor]): A list of actors associated with this node.
        name (str): The name of the node.
        purpose (str): The purpose or function of the node within the network.
        comm(Schema): The communication network to which this node belongs.
    """
    def __init__(self, actors, name: str, purpose: str, comm=None, outs_to_file=False) -> None:
        """
        Initializes a new Node instance.

        Args:
            actors (List[Actor]): A list of actors that are part of this node.
            name (str): The name of the node.
            purpose (str): The purpose of the node in the network.
            comm(Schema): The communication network this node is a part of.

        This method sets up the node with the given actors, name, and purpose. If a
        communication network is provided, it adds the node to that network.
        """
        self.actors = actors
        self.name = name
        self.purpose = purpose
        self.outs_to_file = outs_to_file
        if comm:
            self.comm = comm
            self.comm.add_node(self)
            
    
    async def get_node_completion_gen(self, message: str)-> AsyncGenerator[str, None]:
        """
        An abstract method that must be implemented by subclasses.

        This method should asynchronously process a message through the node.

        Args:
            message (str): The message to be processed by the node.

        Yields:
            The method should yield the results of the message processing.

        This method defines the core functionality of how a node processes a message.
        The specific implementation will depend on the type of node.
        """
        pass

    def save_message_to_file(self, text, directory="C:\\Users\\snbaf\\Documents\\GitHub\\agents\\Markdown Files"):
        """
        This method appends the provided text to the history markdown file in the given directory,
        followed by a line of dashes to separate messages.
        
        :param text: The text message to be saved.
        :param directory: The directory where the history file is located.
        :param file_name: The name of the history file.
        """
        print('APPENDING MESSAGE')
        file_name = self.name + '.md'
        
        # Check if the directory exists
        if not os.path.isdir(directory):
            print("The specified directory does not exist.")
            return
        
        # Construct the full path to the history file
        file_path = os.path.join(directory, file_name)
        
        # Define the separator line
        separator = "-" * 20
        
        # Open the file in append mode and write the text with the separator
        with open(file_path, 'a') as history_file:
            history_file.write(text + "\n")  # Write the text
            history_file.write(separator + "\n")  # Write the separator
        
        print(f"The message has been appended to {file_name}")

    def __repr__(self) -> str:
        """
        Returns a string representation of the Node.

        Returns:
            str: A string representation, showing the name of the node.
        """
        return f"{self.name} Chat"
    
    def __gt__(self, other):
        # Check if 'other' is also an Agent instance
        if isinstance(other, Node):
            # Add an edge from self to other
            if other not in self.comm.nodes:
                other.comm = self.comm
                self.comm.add_node(other)
            self.comm.add_communication_path(self, other)
        return other