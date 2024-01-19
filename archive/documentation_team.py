import sys
sys.path.append('../')

from Communications.Schema import Schema
from Communications.Chats import Chat, ChatOne
from Nodes.Actor import Actor
from Nodes.Agent import Agent, Assistant, Developer
from Nodes.User import User
import re
import asyncio
from Tools import CreateFile, Program, GetFilesInDirectory, OpenFile
comm:Schema = Schema()

swarm_goal = 'To read all the files in a particular set of folders and write documentation for each '


user = ChatOne(actor=User(), comm=comm)


fileReader = ChatOne(actor = Assistant(name='File Documenter', 
                        instructions=f"""You are the File Reader agent. You are provided with a codebase or set of folders. You read the entire set of code inside all of the folders and generate documentation for those codebases. 
                        Make sure you read the entire codebase before doing this. For each folder provided, write README.me that explains what is going on in all the code in the folder. Explain how the code relates to other folders. """,
                        description="Responsible for reading files and writing long important documentation and summaries. Read all files together and write documentation across lots of files. ",
                        functions=[CreateFile, Program, GetFilesInDirectory, OpenFile]),
                        comm=comm)



user > fileReader

comm.startup(user)
