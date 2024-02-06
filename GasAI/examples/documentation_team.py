import sys
sys.path.append('../')

from context import *

comm:Schema = Schema()

swarm_goal = 'To read all the files in a particular set of folders and write documentation for each '


user = User(comm=comm)


fileReader = Assistant(name='File Documenter', 
                        instructions=f"""You are the File Reader agent. You are provided with a codebase or set of folders. You read the entire set of code inside all of the folders and generate documentation for those codebases. 
                        Make sure you read the entire codebase before doing this. For each folder provided, write README.me that explains what is going on in all the code in the folder. Explain how the code relates to other folders. """,
                        description="Responsible for reading files and writing long important documentation and summaries. Read all files together and write documentation across lots of files. ",
                        functions=[CreateFile, Program, GetFilesInDirectory, OpenFile])

dev_team = Chat(actors=[fileReader], name="Documentation Team", description="To write comprehensive documentation about a particular topic")


user > GoalMaker(name='goal maker') > dev_team

comm.startup(user)
