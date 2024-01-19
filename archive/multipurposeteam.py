import sys
sys.path.append('../')

from Communications.Schema import Schema
from Communications.Chats import Chat, ChatOne
from Nodes.Agent import Agent, Assistant, Developer
from Nodes.User import User
from Tools.ToolForge import SearchWebDDGS
from Tools.ToolForge import ExecuteCommand, CreateFile, Program, GetFilesInDirectory, OpenFile, CreateDir
from Tools.ToolImporter import ToolImporter

comm:Schema = Schema()


user = User()

research_agent:Agent= Assistant(name='Research Agent', 
                        instructions="""You are the Research Agent, with the following purpose. Call the research methods and return information""",
                        description="Responsible for searching the web and pulling information",
                        functions=[SearchWebDDGS])


file_agent:Agent= Developer(name='File Agent', 
                        instructions="""You are the File Agent that can read and write files. You work exclusively in the workspace directory, no where else. YOU ARE NOT ALLOWED TO CREATE FILES ANYWHERE BESIDES THE WORKSPACE DIRECTORY. 
                        If the user asks to write a report, follow their guidelines exactly. Do not deviate from the command, and for these reports on individuals, follow the following guidelines:
                        
                        what is their authority, some important quotes or things they have done, and more. Prep the notes so that they are usable for a potential meeting
                        
                        Write all markdown to the /Markdown Files directory. If you cannot find it, call get filesindirectory and navigates
                        """,
                        description="responsbile for reading and writing files",
                        functions=[CreateFile, OpenFile, CreateDir, GetFilesInDirectory])


dev_agent:Agent= Developer(name='Developer Agent', 
                        instructions="""You are the Developer Agent, with the following purpose. You are responsible for running and executing Programs.
                        Before you do anything, GET THE CODE THAT THE USER PROVIDED AND OPEN THAT CODE. ALL FUTURE CODE SHOULD BE WRITTEN BASED ON THE USER CODE
                        YOU CAN ONLY WRITE CODE AND CALL FUNCTIONS. Base all your information from the code examples. 

                        - Write clean and efficient  code.
                        - Structure your code logically
                        - Ensure correct imports according to program structure.
                        - Execute your code to test for functionality and errors, before reporting back to the user.
                        - Anticipate and handle potential runtime errors.
                        - Provide clear error messages for easier troubleshooting.
                        - Debug any issues before reporting the results back to the user.

                        Use function calling whenever necessary to execute your actions. 
                        
                        For all function calls and code, operate in the workspace directory. You are not allowed to create code in any place BESIDES the workspace. 


""",
                        description="responsible for running and executing Python Programs.",
                        functions=[ExecuteCommand, CreateFile, Program,  GetFilesInDirectory, OpenFile, CreateDir])



dev_assistant:Assistant= Assistant(name='Assistant Agent', 
                        instructions="""You are the Assistant Agent, with the following purpose. Communicate the plan and goal. If any Agent has any questions, please respond. Contextualize any plan provided to you with programming information. Keep this short and sweet.""",
                        description="responsible for communicating the project vision. After the goal is completed, this bot will end the chats",
                        functions=[])

# dev_team = Chat(actors=[dev_assistant, dev_agent], name="Multipurpose Team", purpose="To meet the users needs, whatever they may be", comm=comm)

ChatOne(actor=dev_agent, comm=comm).startup()