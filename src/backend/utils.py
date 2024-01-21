from swarmtypes import *
from context import Schema, Developer, Agent, ToolNameDict, User

def create_communication_schema(graph_data: GraphData) -> Schema:
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
            )
        
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

# test = GraphData(nodes=[Node(id='cba589cb-7fea-4c13-8da7-0bbd9c1386d6', type='agent', data=AgentData(agentID='cba589cb-7fea-4c13-8da7-0bbd9c1386d6', agentName='USER', agentInstruction='', agentDescription='', agentTools=[]), position=Position(x=161.89039563573806, y=-39.0), width=142, height=123, selected=False, positionAbsolute=Position(x=161.89039563573806, y=-39.0), dragging=False), Node(id='548960e7-879a-40ff-ae2a-dddfff1b9a89', type='agent', data=AgentData(agentID='548960e7-879a-40ff-ae2a-dddfff1b9a89', agentName='Research Agent', agentInstruction='You are the Research Agent, with the following purpose. Call the research methods and return information', agentDescription='Responsible for searching the web and pulling information', agentTools=['SearchWebDDGS']), position=Position(x=399.4602320447611, y=-27.2042005458797), width=356, height=231, selected=True, positionAbsolute=Position(x=399.4602320447611, y=-27.2042005458797), dragging=False), Node(id='5084cecf-9dca-4f09-bba0-b0ecf24b1ccb', type='agent', data=AgentData(agentID='5084cecf-9dca-4f09-bba0-b0ecf24b1ccb', agentName='Assistant Agent', agentInstruction='You are the Assistant Agent, with the following purpose. Communicate the plan and goal. If any Agent has any questions, please respond. Contextualize any plan provided to you. Keep this short and sweet.', agentDescription='responsible for communicating the project vision. After the goal is completed, this bot will end the chats', agentTools=[]), position=Position(x=625.8525948906218, y=-374.6111405331043), width=356, height=295, selected=False, positionAbsolute=Position(x=625.8525948906218, y=-374.6111405331043), dragging=False)], edges=[], viewport=Viewport(x=-115.83549360740253, y=218.52267141728862, zoom=0.5321850912266797))


# create_communication_schema(test).viz()