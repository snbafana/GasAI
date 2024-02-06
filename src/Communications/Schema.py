from Nodes.User import User
import networkx as nx
import matplotlib.pyplot as plt
from Nodes.UtilityAgents import Splitter, Joiner
from Nodes.Node import Node
from Nodes.Chats import Chat, UtilityNode
import itertools
import logging
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

# Chatmessage Output

# Global dictionary to store tasks
tasks = {}

class Schema:
    """
    A class representing the schema of a communication network. This communication network is made up of nodes, where each node can get some completion 

    Attributes:
        graph (nx.MultiDiGraph): A directed graph representing the network.
        nodes (list[Node]): A list of nodes in the network. Each Node is a type of Chat Group
        autosplitting (bool): Flag indicating whether auto splitting is enabled. This applies when the user is connected to a single output node, so the program will split the user's query into multiple goals. Each of those goals will be passed through the system at the same time. 
    """

    def __init__(self):
        """
        Initializes the Schema with an empty graph and node list.
        """
        self.graph = nx.MultiDiGraph()
        self.nodes = []
        self.autosplitting = False

    def add_node(self, node: Node) -> None:
        """
        Adds a node to the graph and the node list.

        Args:
            node (Node): The node to be added.
        """
        self.graph.add_node(node)
        self.nodes.append(node)

    def remove_node(self, node: Node) -> None:
        """
        Removes a node from the graph.

        Args:
            node (Node): The node to be removed.
        """
        self.graph.remove_node(node)

    def add_communication_path(self, from_node: Node, to_node: Node, weight=1) -> None:
        """
        Adds a directed edge between two nodes in the graph.

        Args:
            from_node (Node): The source node.
            to_node (Node): The destination node.
            weight (int): The weight of the edge (default is 1).
        """
        self.graph.add_edge(from_node, to_node, weight=weight)

    def get_dicts(self) -> dict:
        """
        Converts the graph to a dictionary of dictionaries format.

        Returns:
            dict: A dictionary representation of the graph.
        """
        return nx.to_dict_of_dicts(self.graph)

    def remove_communication_path(self, from_node: Node, to_node: Node) -> None:
        """
        Removes a directed edge between two nodes in the graph.

        Args:
            from_node (Node): The source node.
            to_node (Node): The destination node.
        """
        self.graph.remove_edge(from_node, to_node)

    def remove_paths(self, from_nodes: list[Node], to_nodes: list[Node]) -> None:
        """
        Removes multiple paths between given sets of nodes.

        Args:
            from_nodes (list[Node]): List of source nodes.
            to_nodes (list[Node]): List of destination nodes.
        """
        for n1, n2 in itertools.product(from_nodes, to_nodes):
            self.remove_communication_path(n1, n2)

    def add_paths(self, from_nodes: list[Node], to_nodes: list[Node]) -> None:
        """
        Adds multiple paths between given sets of nodes.

        Args:
            from_nodes (list[Node]): List of source nodes.
            to_nodes (list[Node]): List of destination nodes.
        """
        for n1, n2 in itertools.product(from_nodes, to_nodes):
            self.add_communication_path(n1, n2)
        
    def find_double_outward_connections(self):
        """
        Identifies nodes in the graph with more than one outward connection.

        Returns:
            dict: A dictionary where keys are nodes with double outward connections,
                  and values are lists of tuples representing these connections.
        """
        double_connections = {}
        for node in self.graph.nodes():
            neighbors = list(self.graph.successors(node))
            if len(neighbors) >= 2:
                for i in range(len(neighbors)):
                    for j in range(i+1, len(neighbors)):
                        double_connections.setdefault(node, []).append((neighbors[i], neighbors[j]))
        return double_connections
    

    def find_next_common_node(self, start1:Node, start2:Node):
        graph = self.graph
        if start1 == start2:
            return start1  # The starting nodes are the same

        # Get all reachable nodes from each start node using BFS
        reachable_from_start1 = set(nx.single_source_shortest_path_length(graph, start1).keys())
        reachable_from_start2 = set(nx.single_source_shortest_path_length(graph, start2).keys())

        # Find the intersection of these sets to get common nodes
        common_nodes = reachable_from_start1.intersection(reachable_from_start2)

        if not common_nodes:
            return None  # No common node found

        # Optional: Find the closest common node (minimum combined distance)
        min_distance = float('inf')
        closest_common_node = None
        for node in common_nodes:
            distance = nx.shortest_path_length(graph, start1, node) + nx.shortest_path_length(graph, start2, node)
            if distance < min_distance:
                min_distance = distance
                closest_common_node = node

        return closest_common_node

          
    def get_connected_nodes(self, node):
        """
        Retrieves a list of nodes connected to the given node in the network.

        Args:
            node (Node): The node for which connected nodes are to be found.

        Returns:
            list[Node]: A list of nodes that are directly connected to the given node.
        """
        connected_nodes = []
        for target in self.graph[node]:
            connected_nodes.append(target)

        return connected_nodes
        
    async def system_pass(self, message, starting_node:Node, threadname='main'):
        """
        Asynchronously processes a message through the network starting from a specific node.

        Args:
            message (str): The message to process.
            starting_node (Node): The starting node for processing.
            threadname (str): The name of the thread.

        This method traverses the network from the starting node, processing the message
        through each connected node. If auto-splitting is enabled and the node is a User node,
        the message is split and processed accordingly.
        """
        node:Node = starting_node  
        connected_nodes = self.get_connected_nodes(node)
  
        while connected_nodes != []:
            # print("RUNNING")
            connected_nodes = self.get_connected_nodes(node)
            if isinstance(node, UtilityNode):
                
                if node.placetype == Splitter:
                    
                    splitter = node.build_splitter(connected_nodes)
                    splittermsg = ""
                    # print("STARTING SPLITTER")
                    async for s in splitter.get_completion(message, threadname=threadname):
                        print(s + '\n')
                        print('_'*15)
                        splittermsg = s
                        
                    # print("ENDED SPLITTER")
                                                    
                    active_generators = splitter.get_splitter_tasks()
                    gen_messages = ["" for i in active_generators]
                    final_nodes = []
                    # print("Generators: ", active_generators)
                    while active_generators:
                        for i, gen in enumerate(active_generators):
                            try:
                                value = await gen.__anext__()
                                if isinstance(value, Node):
                                    final_nodes.append(value)    
                                    pass
                                else:
                                    # print(gen, " : ", value)
                                    print(value)
                                    print('_'*15)
                                    gen_messages[i] = value
                            except StopAsyncIteration:
                                
                                active_generators.remove(gen)
                                
                    gen_messages_str = "\n".join(gen_messages)

                    message_content = f"This is a summary of the history so far. Complete the requests mentioned in the information. Do whatever is necessary\n\n{message}\n\n{splittermsg}\n\n{gen_messages_str}"

                    message = f"""{message_content}"""
                    
                    # print('final nodes, ', final_nodes)
                    
                    node = final_nodes[0]

                elif node.placetype == Joiner:
                    
                    joiner = node.build_joiner()
                    async for s in joiner.get_completion(message, threadname=threadname):
                        print(s + '\n')
                        print('_'*15)
                        message = s
                    
                    if connected_nodes != []:    
                        node =  connected_nodes[0]
                    else:
                        print(message)
                        return message
                        print("Completed ")
                    
            
            else:  
                async for m in node.get_completion(message, threadname=threadname):
                    print(message)
                    print('_'*15)
                    message = m
                    
                if connected_nodes != []:    
                    node =  connected_nodes[0]
                else:
                    print(message)
                    return message
                    print("Completed ")

    async def singular_system_pass(self, message, starting_node:Node, threadname='main', splitter_id=None):
        """
        Asynchronously processes a message through a singular path in the network.

        Args:
            message (str): The message to process.
            starting_node (Node): The starting node for processing.
            threadname (str): The name of the thread.

        Yields:
            The processed message after passing through each node.

        Unlike system_pass, this method processes the message through a single path in the
        network, following one connection at a time from the starting node.
        """
        node:Node = starting_node  
        connected_nodes = [1]
  
        while connected_nodes != []:
            connected_nodes = self.get_connected_nodes(node)
              
            async for m in node.get_completion(message, threadname=threadname):
                message = m
                yield m
            
            if connected_nodes != []:
                node =  connected_nodes[0]
                if isinstance(node, UtilityNode) and node.placetype == Joiner and node.id == splitter_id:
                    yield node
                    return
                        
        
        return
    



    def viz(self):
        """
        Visualizes the graph representing the network using Matplotlib.

        This method draws the network graph, illustrating the nodes and their connections.
        """
        nx.draw(self.graph)
        plt.show()
        
    def startup(self, starting_node:Node, message=''):
        """
        Initiates the message processing in the network asynchronously.

        Args:
            starting_node (Node): The node from which to start processing.

        No return value. Initiates the asynchronous message processing.
        """
        return asyncio.run(self.system_pass(message=message, starting_node=starting_node))

    async def system_pass_gen(self, message, starting_node:Node, threadname='main'):
           
        """
        Asynchronously processes a message through the network starting from a specific node.

        Args:
            message (str): The message to process.
            starting_node (Node): The starting node for processing.
            threadname (str): The name of the thread.

        This method traverses the network from the starting node, processing the message
        through each connected node. If auto-splitting is enabled and the node is a User node,
        the message is split and processed accordingly.
        """
        node:Node = starting_node  
        connected_nodes = self.get_connected_nodes(node)
  
        while connected_nodes != []:
            connected_nodes = self.get_connected_nodes(node)
            if isinstance(node, UtilityNode):
                
                if node.placetype == Splitter:
                    
                    splitter = node.build_splitter(connected_nodes)
                    splittermsg = ""
                    async for s in splitter.get_completion(message, threadname=threadname):
                        yield s
                        splittermsg = s
                                                    
                    active_generators = splitter.get_splitter_tasks()
                    gen_messages = ["" for i in active_generators]
                    final_nodes = []
                    yield "Generators:  " + str(active_generators)
                    while active_generators:
                        for i, gen in enumerate(active_generators):
                            try:
                                value = await gen.__anext__()
                                if isinstance(value, Node):
                                    final_nodes.append(value)    
                                    pass
                                else:
                                    yield value                                    
                                    gen_messages[i] = value
                            except StopAsyncIteration:
                                
                                active_generators.remove(gen)
                                
                    gen_messages_str = "\n".join(gen_messages)

                    message_content = f"This is a summary of the history so far. Complete the requests mentioned in the information. Do whatever is necessary\n\n{message}\n\n{splittermsg}\n\n{gen_messages_str}"

                    message = f"""{message_content}"""
                    
                    print('final nodes, ', final_nodes)
                    
                    node = final_nodes[0]

                elif node.placetype == Joiner:
                    
                    joiner = node.build_joiner()
                    async for s in joiner.get_completion(message, threadname=threadname):
                        yield s
                        message = s
                    
                    if connected_nodes != []:    
                        node =  connected_nodes[0]
                    else:
                        yield "Completion"
                    
            
            else:  
                async for m in node.get_completion(message, threadname=threadname):
                    yield m
                    message = m
                    
                if connected_nodes != []:    
                    node =  connected_nodes[0]
                else:
                    yield "Completion"

    async def start(self, starting_node:Node):

        async for message in self.system_pass_gen(starting_node=starting_node, message=""):
            yield "data:" + message + "\n\n"
        