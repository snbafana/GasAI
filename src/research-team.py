import sys
sys.path.append('../')

from Communications.Schema import Schema
from Nodes import  Developer, Assistant, User, SplitJoinPair, Chat, Agent
import re
import asyncio
from Tools.ToolForge import CreateDirective, SearchWebDDGS, SiteScraper
from Tools.ToolForge import ExecuteCommand, CreateFile, Program, GetFilesInDirectory, OpenFile, CreateDir
comm:Schema = Schema()

swarm_goal = 'To answer to the users needs in all forms of information gathering, email and file writing, and networking/meeting aid'


user = User(comm=comm)

research_node1 = Assistant(name='Research Agent', 
                        instructions=f"""You are the Research Agent, operating for the following swarm goal: {swarm_goal}
                                        You take in  queries/info and research the info through your function calling. 
                                        Return all the information you gained like links, web info, and most specifically website content. Function call concisely, as little as possible. 
                                        But you must do it. Cite all sources, and query with relevance. Do not ask for any advice. Just execute all the research you can do, navigate as many website, and return all your information""",
                        description="Responsible for searching the web and pulling information",
                        functions=[SearchWebDDGS])

research_node2 = Assistant(name='Research Agent', 
                        instructions=f"""You are the Research Agent, operating for the following swarm goal: {swarm_goal}
                                        You take in  queries/info and research the info through your function calling. 
                                        Return all the information you gained like links, web info, and most specifically website content. Function call concisely, as little as possible. 
                                        But you must do it. Cite all sources, and query with relevance. Do not ask for any advice. Just execute all the research you can do, navigate as many website, and return all your information""",
                        description="Responsible for searching the web and pulling information",
                        functions=[SearchWebDDGS])


file_node = Assistant(name='File Agent', 
                        instructions=f"""You are the File Agent, operating for the following swarm goal: {swarm_goal} 
                        You take in information and links from the research agent, and write a markdown report that summarizes all that was learned. Some questions to think about are: 
                        If the user asks to write a report, follow their guidelines exactly. Do not deviate from the command, and for these reports on individuals, follow the following guidelines:
                        what is their authority, some important quotes or things they have done, and more. Prep the notes so that they are usable for a potential meeting
                        
                        You can read and write files. Write files to the "Markdown Files files directory. If you cannot find it, then call getfilesindirectory to find it""",
                    
                        description="responsbile for reading and writing files, most specifically, writing the report files",
                        functions=[CreateFile, GetFilesInDirectory])


splitter, joiner = SplitJoinPair()

user > splitter
splitter > research_node1 > joiner
splitter > research_node2 > joiner
joiner > file_node

comm.startup(starting_node=user)
