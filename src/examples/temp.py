from context import *

comm:Schema = Schema()

# swarm_goal = 'To answer to the users needs in all forms of information gathering, email and file writing, and networking/meeting aid'


user = User(comm=comm)

research_node1 = Assistant(name='Research Agent', 
                        instructions=f"""You are the Research Agent
                                        You take in  queries/info and research the info through your function calling. 
                                        Return all the information you gained like links, web info, and most specifically website content. Function call concisely, as little as possible. 
                                        But you must do it. Cite all sources, and query with relevance. Do not ask for any advice. Just execute all the research you can do, and return all your information
                                        Make sure to ansewr the question. That is key. Info + Fact.  Include a lot of links.""",
                                        description="Responsible for searching the web and pulling information",

                        functions=[SearchWebDDGS])

research_node2 = Assistant(name='Research Agent', 
                        instructions=f"""You are the Research Agent
                                        You take in  queries/info and research the info through your function calling. 
                                        Return all the information you gained like links, web info, and most specifically website content. Function call concisely, as little as possible. 
                                        But you must do it. Cite all sources, and query with relevance. Do not ask for any advice. Just execute all the research you can do, and return all your information
                                        Make sure to ansewr the question. That is key.  Info + Fact.  Include a lot of links.""",
                        description="Responsible for searching the web and pulling information",
                        functions=[SearchWebDDGS])

research_node3 = Assistant(name='Research Agent', 
                        instructions=f"""You are the Research Agent
                                        You take in  queries/info and research the info through your function calling. 
                                        Return all the information you gained like links, web info, and most specifically website content. Function call concisely, as little as possible. 
                                        But you must do it. Cite all sources, and query with relevance. Do not ask for any advice. Just execute all the research you can do, and return all your information
                                        Make sure to ansewr the question. That is key.  Info + Fact. Include a lot of links.""",
                        description="Responsible for searching the web and pulling information",
                        functions=[SearchWebDDGS,])


# file_node = Assistant(name='File Agent', 
#                         instructions=f"""You are the File Agent
                        
#                         You can read and write files. Write files to the "Markdown Files files directory. If you cannot find it, then call getfilesindirectory to find it""",
                    
#                         description="responsbile for reading and writing files, can also analyze code files",
#                         functions=[CreateFile, Program, GetFilesInDirectory, OpenFile, GetCurrentDirectory])


# dev_team = Chat(actors=[research_node2, user], name="Report Team", description="To write comprehensive scientific report about a particular topic")


# user > dev_team


# goals = GoalMaker(name="Goal Maker")

s, j = SplitJoinPair()



# research_chat = Chat(actors=[research_node2, file_node], name="Research Team", description="To research about something in depth and write comprehensive info about a particular topic")

user > s

s > research_node1 > j
s > research_node2 > j 

with open("researchtest.txt", 'r') as r:
    lines = r.readlines()

print(lines)
with open('out.md', 'a+') as a:
    
    for line in lines:

        a.write(comm.startup(starting_node=s, message=line)[20:])
        a.write("------------------------------------------")

# comm.startup(starting_node=user)