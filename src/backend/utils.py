from swarmtypes import *
from context import Schema, Developer, Agent, ToolNameDict, User
import json
import asyncio

def create_communication_schema(graph_data: GraphData):
    schema = Schema()

    # Create a mapping of Pydantic node IDs to Node instances
    node_mapping = {}
    for pydantic_node in graph_data.nodes:
        agent_data = pydantic_node.data
        
        # Convert tool names using ToolNameDict
        tools = [ToolNameDict.get(tool_name, None) for tool_name in agent_data.agentTools]
        tools = [tool for tool in tools if tool is not None]  # Filter out None values if any tool is not found in ToolNameDict

        if agent_data.agentName == "USER":
            node = User(comm=schema)
            starting_node = node
        else:
            node = Agent(
                name=agent_data.agentName,
                instructions=agent_data.agentInstruction,
                description=agent_data.agentDescription,
                functions=tools,
                comm=schema
            ).create_openai_agent()
        
        schema.add_node(node)
        node_mapping[pydantic_node.id] = node

    

    # Add edges to the schema
    for edge in graph_data.edges:
        from_node = node_mapping.get(edge.source)
        to_node = node_mapping.get(edge.target)
        
        
        if from_node and to_node:
            from_node > to_node


    if starting_node is None:
        raise ValueError("Starting node (User) not found in the provided GraphData")

    return schema, starting_node


async def test():
    with open('JsonFiles/swarm_data.json', 'r') as f:
        data = json.loads(f.read())
        test = GraphData(**data)

        schmea, u = create_communication_schema(test)
        async for m in  schmea.start(starting_node=u):
            print(m)
    
def main():
    import requests

    url = "http://localhost:8000/stream/"

    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(None, decode_unicode=True):
            if chunk:
                print(chunk, end='', flush=True)
    
if __name__ == "__main__":
    asyncio.run(test())