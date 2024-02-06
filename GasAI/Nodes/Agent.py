from instructor import OpenAISchema
from typing import List
from openai import OpenAI
import asyncio
import time
import inspect
import logging
from typing import AsyncGenerator
from typing_extensions import Self
import os
from .Node import Node

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.WARNING)

# OpenAI client initialization with API key
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

class Agent(Node):
    """An Agent class that extends Actor for interaction with OpenAI's API.

    This class manages the lifecycle of agents including creation, message sending,
    and handling responses from OpenAI's API.

    Attributes:
        name (str): The name of the agent.
        functions (List[OpenAISchema]): A list of functions that the agent can perform.
        model (str): The model used by OpenAI for this agent.
        instructions (str): Instructions for the agent.
        description (str): A description of the agent.
        threads (dict): Dictionary to manage threads for asynchronous operations.
    """

    def __init__(self, name: str, instructions: str, description: str, functions: List[OpenAISchema] = [], model: str = "gpt-4-1106-preview", id=0, **kwargs) -> None:
        """
        Initialize an Agent instance.

        Args:
            name (str): The name of the agent.
            instructions (str): Instructions for the agent.
            description (str): A description of the agent.
            functions (List[OpenAISchema]): A list of functions that the agent can perform.
            model (str): The model used by OpenAI for this agent.
            **kwargs: Additional keyword arguments.
        """
        self.name = name
        self.functions = functions
        self.model = model
        self.instructions = instructions
        self.description = description
        self.threads = {}
        self.id = id



        super().__init__(name=name, description=description, **kwargs)

    def __repr__(self) -> str:
        """
        String representation of the Agent.

        Returns:
            str: The name of the agent.
        """
        return self.name

    def create_openai_agent(self) -> Self:
        """
        Creates an OpenAI assistant instance with the specified configuration.

        Returns:
            Agent: The current instance of Agent.
        """
        self.tools = [{"type": "function", "function": f.openai_schema} for f in self.functions]
        self.openai_agent = client.beta.assistants.create(
            name=self.name, instructions=self.instructions, model=self.model, tools=self.tools
        )
        return self

    async def handle_completion(self, message: str, run, threadname='main', color_output=True) -> AsyncGenerator[str, None]:
        """
        Asynchronously generates completion from OpenAI's API.

        Continuously monitors and processes the status of the run object, handling any
        required actions such as function executions and yielding the outputs. This
        method also allows for toggling colored output through ANSI codes.

        Args:
            message: The input message to be processed.
            run: The run object to monitor the status of the message processing.
            threadname: The name of the thread for processing the message, defaults to 'main'.
            color_output: If True, includes ANSI color codes in the output, defaults to True.

        Yields:
            The output from the OpenAI API or the processed results from tool calls.

        Raises:
            Exception: If the run status is 'failed', indicating an error occurred during processing.
        """
        
        logging.info(f"Starting message completion for {self.name} in thread '{threadname}'")
        
        # Loop to continuously check and process the run's status
        while True:
            print("running")
            # Await run completion if it's queued or still in progress
            while run.status in ['queued', 'in_progress']:
                run = client.beta.threads.runs.retrieve(thread_id=self.threads[threadname].id, run_id=run.id)
                await asyncio.sleep(1)

            logging.info(f"Run status for {self.name} in thread '{threadname}': {run.status}")

            if run.status == "requires_action":
                # Handle actions required by the run (e.g., function calls)
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for tool_call in tool_calls:
                    func_name = f'{self.name}\n ' + str(tool_call.function) + '\n'
                    yield func_name
                    func_output = ''
                    func = next(func for func in self.functions if func.__name__ == tool_call.function.name)

                    try:
                        func = func(**eval(tool_call.function.arguments))

                        if inspect.isasyncgenfunction(func.run):
                            final_output = ""
                            async for out in func.run():
                                # print(out)
                                yield out
                                final_output += out[0] if isinstance(out, tuple) else str(out)
                            func_output = final_output
                        elif inspect.iscoroutinefunction(func.run):
                            func_output = await func.run()
                        elif callable(func.run):
                            func_output = func.run()
                        else:
                            func_output = func_output

                        if asyncio.iscoroutinefunction(func_output):
                            func_output = await func_output

                    except Exception as e:
                        func_output = "Error: " + str(e)
                        logging.error(f"Error in executing tool function for {self.name}: {e}")

                    
                    if color_output:
                        yield f"\033[31m{func_name} : {func_output}\033[0m"
                    else:
                        yield f"{func_name}: {func_output}"

                    tool_outputs.append({"tool_call_id": tool_call.id, "output": func_output})

                logging.info(f"Submitting tool outputs for {self.name} in thread '{threadname}'")
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.threads[threadname].id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                run = client.beta.threads.runs.retrieve(
                    thread_id=self.threads[threadname].id,
                    run_id=run.id
                )

            elif run.status == "failed":
                error_message = f"Run failed for {self.name} in thread '{threadname}'. Error: {run.last_error}"
                logging.error(error_message)
                raise Exception(error_message)

            elif run.status == "queued":
                time.sleep(1)
                logging.info(f"Run queued for {self.name} in thread '{threadname}', waiting...")

            else:
                messages = client.beta.threads.messages.list(thread_id=self.threads[threadname].id)
                assistant_message = messages.data[0].content[0].text.value

                # print(f'\033[34m{self.name}\n {self.openai_agent.name}: {assistant_message}\033[0m')

                if color_output:
                    yield f'\033[34m{self.name}\n {self.openai_agent.name}: {assistant_message}\033[0m'
                else:
                    yield f'{self.name}\n {self.openai_agent.name}: {assistant_message}'

                logging.info(f"Completion received for {self.name} in thread '{threadname}'")
                return

    async def get_completion(self, message: str, threadname='main') -> AsyncGenerator[str, None]:
        """
        Asynchronous generator method for sending a message.

        Args:
            message (str): The message to be sent.
            threadname (str): The name of the thread (default is 'main').

        Yields:
            The response from the OpenAI API or the yielded values from get_completion.
        """
        logging.info(f"Sending message in '{threadname}' thread with Actor: {self.name}")

        # Check if the thread already exists, if not, create a new one
        if self.threads == {}:
            logging.info(f"Creating a new thread '{threadname}' for Actor: {self.name}")
            self.threads[threadname] = client.beta.threads.create()
        elif threadname != 'main' and threadname not in self.threads:
            logging.info(f"Creating a new thread '{threadname}' for Actor: {self.name}")
            self.threads[threadname] = client.beta.threads.create()

        logging.info(f"Creating a new message in thread '{threadname}' for Actor: {self.name}")

        # Create a new message in the thread
        message_creation_response = client.beta.threads.messages.create(
            thread_id=self.threads[threadname].id,
            role="user",
            content=message
        )
        logging.info(f"Message created with ID {message_creation_response.id} in thread '{threadname}'")

        # Run the thread
        run_creation_response = client.beta.threads.runs.create(
            thread_id=self.threads[threadname].id,
            assistant_id=self.openai_agent.id,
        )
        logging.debug(f"Run created with ID {run_creation_response.id} in thread '{threadname}'")

        # Iterate through the responses from handle_completion
        async for m in self.handle_completion(message, run_creation_response, threadname):
            # print('time')
            if isinstance(m, tuple):
                logging.debug(f"Yielding tuple response from handle_completion in thread '{threadname}'")
                yield m[0]  # Yield the first element of the tuple
            else:
                logging.debug(f"Yielding response from handle_completion in thread '{threadname}'")
                yield m

        logging.info(f"Message sending completed in thread '{threadname}' for Actor: {self.name}")
        return


class Developer(Agent):
    """Represents a specialized type of Agent with additional functionalities for developers."""

    def __init__(self, name: str, instructions: str, description: str, functions: List[OpenAISchema] = [], model: str = "gpt-4-1106-preview", **kwargs):
        """Initializes a Developer instance.

        Args:
            name, instructions, description, functions, model: Inherits from Agent.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(name, instructions, description, functions, model, **kwargs)
        self.create_openai_agent()

class Assistant(Agent):
    """Represents a specialized type of Agent tailored for assistant-like roles."""

    def __init__(self, name: str, instructions: str, description: str, functions: List[OpenAISchema] = [], model: str = "gpt-4-1106-preview", **kwargs):
        """Initializes an Assistant instance.

        Args:
            name, instructions, description, functions, model: Inherits from Agent.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(name, instructions, description, functions, model, **kwargs)
        self.create_openai_agent()