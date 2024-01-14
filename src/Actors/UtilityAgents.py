from typing import List
from instructor import OpenAISchema
from .Agent import Agent
from .Actor import Actor
from .User import User
from instructor import OpenAISchema
from pydantic import Field
from typing import Literal

from typing import AsyncGenerator

tasks = {}


class Decider(Agent):
    def __init__(self, chat, threadname:str='main', goal:str='', model="gpt-4-1106-preview", **kwargs) -> None:
        self.chat = chat
        self.goal = goal
        self.threadname = threadname
        self.actors = chat.actors
        self.goal_achieved = False
        self.name = chat.name + " Decider Agent"
        stringlist = "\n".join([f"{num}. {values['name']} - {values['description']}" for num, values in self.get_descriptions().items()])
        print(stringlist)
        instructions=f"""You are the Decider Agent, named {self.name}. 
                        You operate in a groupchat that works toward the following purpose: {chat.purpose}
                        Based on the provided message, select the agent that makes the most sense for achieving the particular goal that you want to accomplish. 
                        The goal will be provided. If you want to get feedback on if you have achieved the goal, please ask the user, by not calling a function and waiting for feedback. 
                        Here are the following agents you can select from. Use the function calling EACH time to select the agent. 
                
                        {stringlist}"""
        description = "Decides the next speaker"
        functions = [self.build_decider_tool()]
                        
        super().__init__(self.name, instructions, description, functions, model, **kwargs)
        self.create_openai_agent()
        
    
    def get_descriptions(self) -> dict:
        """
        Retrieves descriptions of all actors involved in the chat.

        Returns:
            dict: A dictionary containing descriptions of actors with keys as actor indices
                  and values as dictionaries describing the actors.
        """
        descs = {}
        for i, actor in enumerate(self.actors):
            if isinstance(actor, User):
                descs[i] = {"name": "User", "description": "The human user, providing user input and controls the conversation", "agent": actor}
            elif isinstance(actor, Agent):
                descs[i] = {"name": actor.name, "description": actor.description, "agent": actor}
            
        return descs
    
    def build_decider_tool(self) -> OpenAISchema:
        """
        Builds a decider agent for managing the flow of messages in the chat.
        
        The method initializes a decider agent with specific instructions and functions 
        based on the provided goal. The decider agent is responsible for determining 
        which actor should receive the message next in the chat flow.
        """
        descriptions = self.get_descriptions()
        outerself = self
        
        class ChooseNextSpeaker(OpenAISchema):
            f"""From a particular message, choose which agent should recieve the message that you just recieved. 
            
            If the goal, "{outerself.goal}", has been achieved then demonstrate so in the goal_achieved variable. Or, if there is nothing else to do
            set the goal_achieved to true. 
            
            Make these decisions as soon as you believe some output was given. If an agent asks a question in their message, RESPOND IN YOUR MESSAGE. YOU MANAGE CONVERSATIONAL FLOW. 
            Other agents cannot see all the messages that you see, they are conversing with you 1 on 1. Thus, make sure to pass ALL relevant information in the message variable
            
            Do not over contextualize, keep the flow in and out as smooth as possible and short but hyperspecific. 
            """
            chain_of_thought: str = Field(...,
                                        description="Think step by step to determine the correct recipient and "
                                                    "message.")
            r_id:int = Field(..., description="The ID number of the person that you are going to send a message to")
            message: str = Field(...,
            description="Content that you are sending to the new agent. This should be ALL THE CONTENT FROM THE PREVIOUS MESSAGE THAT YOU RECIEVED")
            
            goal_achieved:Literal['true', 'false'] = Field(..., description="true if goal has been achieved otherwise false")

            async def run(self) -> AsyncGenerator[str, None]:
                # Check if the goal has been achieved
                if self.goal_achieved == 'false':
                    # If not, then send a new message to the agent that you selected
                    self.message = f"{self.message}"
                    print(descriptions[self.r_id]["agent"])
                    async for m in  descriptions[self.r_id]["agent"].send_message_gen(self.message, threadname=outerself.threadname):
                        yield m
                else:
                    # If there has been an achievement, then yield the final message
                    outerself.goal_achieved = True
                    yield f"Goal has been achieved: {self.message}"
                
                return 
        
        return ChooseNextSpeaker  
    
    def build_user_input(self) -> OpenAISchema:
        class GetUserInput(OpenAISchema):
            f"""If you have a question, you are able to ask the user through this function. 
            """
            chain_of_thought: str = Field(...,
                                        description="Think step by step to determine the correct reason for this "
                                                    "message.")
            message: str = Field(...,
            description="Question that you have for the user")
            
            async def run(self) -> AsyncGenerator[str, None]:
               yield input(self.message + ": ")
               return
               
        return GetUserInput
        
class Splitter(Agent):
    def __init__(self, name:str, descriptions, out_nodes, comm, model: str = "gpt-4-1106-preview", **kwargs) -> None:
        self.name=name 
        
        stringlist = "\n".join([f"{num}. {values['name']} - {values['description']}" for num, values in descriptions.items()])
        
        
        instructions=f"""You are a Splitter Agent. 
        Based on the provided message, split the information into messages for the recipient agents, so they can execute their tasks. If there is only one recipent agent, split the information into all the subgoals that can be accomplished, 
        so multiple versions of the recipient agent can work together. 
        The goal will be provided. Here are the following agents you can select from. Use the function calling to split up the message for the agents. That is all you have to do. IMPORTANT: Do not call functions more than once.
        Include thorough explanations of the goals, and return those goals. As much info as possible 

        {stringlist}

        Produce 3 subgoals at max. Only call this function ONCE.
        """
        
        description="Splits content for multiple speakers"
                
        functions=[self.create_splitting_tool(out_nodes, comm, descriptions)]
        
        super().__init__(self.name, instructions, description, functions, model, **kwargs)
        self.create_openai_agent()
        
        
    def create_splitting_tool(self, out:list, outerself, descriptions) -> OpenAISchema:
        splitterself = self
        """
        Creates a Splitter class based on the number of output nodes provided.

        This function dynamically creates a subclass of OpenAISchema named Splitter. 
        The Splitter class is designed to take an input message and delegate tasks to other nodes.

        Args:
            out (list[Node]): A list of output nodes to which the splitter will delegate tasks.

        Returns:
            OpenAISchema: A dynamically created Splitter class.

        The Splitter class behavior varies depending on the number of output nodes:
        - If there is only one node, the Splitter delegates tasks equally among the same group of agents.
        - If there are multiple nodes, the Splitter splits tasks based on the descriptions of the output nodes.

        The Splitter class contains:
        - A `chain_of_thought` field to describe the decision-making process.
        - A `messages` field containing a list of strings, where each string represents a task or a detailed message for the next agent.
        - An asynchronous `run` method that implements the task delegation logic.
        """
        if len(out) == 1:
            class Splitter(OpenAISchema):
                """Take the input message and delegate the tasks among the same group of agents. THIS is only called when there is one node attached to the splitter. 
                Split the tasks equally."""
                chain_of_thought: str = Field(...,
                                            description="Think step by step to determine the correct"
                                                        "message.")
                messages: list[str] = Field(...,
                description="""A list of strings where each string is the task that needs to be completed""")
                
                rejoining:Literal['true', 'false'] = Field(..., description="true if the tasks will be rejoining one another after completion, false otherwise")

                
                async def run(self) -> str:
                    tasks[splitterself.name] = []

                    for message in self.messages:
                        tasks[splitterself.name].append(outerself.singular_system_pass(message, starting_node=out[0], threadname=message))
                
                    return 'Task Delegation Complete' 
            return Splitter
        else:
            class Splitter(OpenAISchema):
                """Take the input message and delegate the tasks among the output agents provided to you in the prompt. You do not need to give tasks to each agent. 
                Split the tasks according to their descriptions."""
                chain_of_thought: str = Field(...,
                                            description="Think step by step to determine the correct recipients and "
                                                        "message.")
                messages: list[str] = Field(...,
                description="""A list of strings where each string is the corresponding message for the next agent. Each string's index should correspond to the recipient agent's id. Each string should be extremely information dense""")
                
                rejoining:Literal['true', 'false'] = Field(..., description="true if the tasks will be rejoining one another after completion, false otherwise")

                
                async def run(self) -> str:
                    dic:dict[Actor, str] = {descriptions[i]["node"]:e for i, e in enumerate(self.messages)}
                    tasks[splitterself.name] = []

                    for node, message in dic.items():
                        tasks[splitterself.name].append(outerself.singular_system_pass(message, starting_node=node, threadname=message))
                
                    return "Task Delegation Complete" 
            return Splitter
    
    def get_splitter_tasks(self) -> list[AsyncGenerator]:
        return tasks[self.name]
    
class Joiner(Agent):
    def __init__(self, name: str, instructions: str, description: str, functions: List[OpenAISchema] = ..., model: str = "gpt-4-1106-preview", **kwargs) -> None:
        super().__init__(name, instructions, description, functions, model, **kwargs)
        
class GoalMaker(Agent):
    def __init__(self, name: str, instructions: str, description: str, functions: List[OpenAISchema] = ..., model: str = "gpt-4-1106-preview", **kwargs) -> None:
        super().__init__(name, instructions, description, functions, model, **kwargs)