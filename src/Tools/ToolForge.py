from instructor import OpenAISchema
from pydantic import Field
import subprocess
from typing import List
import os
from bs4 import BeautifulSoup
import requests
import re
import asyncio


def remove_non_utf8_characters(text):
    """
    Remove non-UTF-8 characters from the given text.

    Args:
    text (str): The text to be processed.

    Returns:
    str: The text with non-UTF-8 characters removed.
    """
    # Encode the text to UTF-8, then decode it back. This will remove non-UTF-8 characters.
    return text.encode('utf-8', 'ignore').decode('utf-8')

def preprocess(text:str) -> str:
    """Removes redundant characters and leaves only raw text

    Args:
        text (str): _description_
    """
    text:str = text.replace('\n', ' ')
    text:str = re.sub('\s+', ' ', text)

    return remove_non_utf8_characters(text)


def search(query) -> str:
    API_KEY = os.environ['GOOGLESEARCH_API_KEY']
    SEARCH_ENGINE_ID = '226631df8b46341cd'
    start=0

    print("QUERY: ", query)

    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"


    data = requests.get(url).json()

    search_items = data.get("items")
    final = """"""
    
    link1, link2, link3, *rest_of_links = search_items
    search_items = [link1, link2, link3] #*random.sample(rest_of_links, k=2)
    final = []
    # iterate over 10 results found
    for i, search_item in enumerate(search_items, start=1):
        try:
            long_description = search_item["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            long_description = "N/A"
            
        # get the page title
        title = search_item.get("title")
        # page snippet
        snippet = search_item.get("snippet")
        # alternatively, you can get the HTML snippet (bolded keywords)
        html_snippet = search_item.get("htmlSnippet")
        # extract the page url
        link = search_item.get("link")
        final.append({'title':title, 'snippet':snippet, 'long_description': long_description, 'link':link})
        # print the results

    return str(final)

def scrape(url)->str:
    
    soup = None


    response = requests.get(url)

    # If the request was successful (status code 200)
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

    if soup is None:
        return "Failed to load page or page content is not accessible."

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = preprocess('\n'.join(chunk for chunk in chunks if chunk))
    words = text.split(" ")
    if len(words) > 14000:
        text = " ".join([words[i] for i in range(14000)])
        
    
    return text

class ExecuteCommand(OpenAISchema):
    """Run any command from the terminal. If there are too many logs, the outputs might be truncated."""
    command: str = Field(
        ..., description="The command to be executed."
    )

    async def run(self):
        """Executes the given command and captures its output and errors."""
        try:
            # Splitting the command into a list of arguments
            
            command_args = self.command.split()
            # if command_args[0] == 'python':
            #     command_args[1] = 'workspace/' + command_args[1]

            # Executing the command
            result = subprocess.run(
                command_args,
                text=True,
                capture_output=True,
                check=True
            )
            
            
            
            return "Executed successfully with this terminal output: " + result.stdout
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e.stderr}"

class CreateDir(OpenAISchema):
    """Creates a folder or directory with the appropriate name."""
    folder_name:str = Field(..., description="the name of the folder and the file path from your current directory if needed")
    
    async def run(self):
        os.makedirs(self.folder_name)
        return self.folder_name + " created"
    
class CreateFile(OpenAISchema):
    """
    File to be written to the disk with an appropriate name and file path, containing code that can be saved and executed locally at a later time.
    """
    file_name: str = Field(
        ..., description="The name of the file including the extension and the file path from your current directory if needed."
    )
    body: str = Field(..., description="Correct contents of a file")

    async def run(self):
        
        # ensure_workspace_dir()
        
        # Extract the directory path from the file name
        directory = os.path.dirname(self.file_name)

        # If the directory is not empty, check if it exists and create it if not
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # # Adjust file path to include workspace directory
        # workspace_file_path = os.path.join("workspace", self.file_name)

        with open(self.file_name, "w") as f:
            f.write(self.body)

        return "File written to " + self.file_name

class Program(OpenAISchema):
    """
    Set of files that represent a complete and correct program. This environment has access to all standard Python packages and the internet.
    """
    chain_of_thought: str = Field(...,
        description="Think step by step to determine the correct actions that are needed to implement the program.")
    files: List[CreateFile] = Field(..., description="List of files")

    async def run(self):
        outputs = []
        for file in self.files:
            outputs.append(asyncio.create_task(file.run()))
        
        final = []
        for output in outputs:
            final.append(await output)

        return str(final)
  
class GetFilesInDirectory(OpenAISchema):
    """Get all the files in a directory"""
    dir_path:str = Field(..., description="the path to the directory that you want to look in")
    async def run(self):
        return str(os.listdir(self.dir_path))
  
class OpenFile(OpenAISchema):
    """
    Getting the content from a file. This information is always important
    """
    file_name: str = Field(
        ..., description="The name of the file including the extension and the file path from your current directory if needed."
    )
    async def run(self):
        with open(self.file_name, 'r') as r:
            return r.read()


from duckduckgo_search import DDGS

class SearchWeb(OpenAISchema):
    """Search the web with a search phrase and return the results."""

    phrase: str = Field(..., description="The search phrase you want to use. Optimize the search phrase for an internet search engine.")

    # This code will be executed if the agent calls this tool
    async def run(self):
    #   with DDGS() as ddgs:
    #     return str([r for r in ddgs.text(self.phrase, max_results=3)])
        return search(self.phrase)
    
class CreateDirective(OpenAISchema):
    """Take in user input and create a directive with the breakdown of goals and additional information. Be as specific as possible. Remember that user does not have access to the output of this function. You must send it back to him after execution."""
    goals: str = Field(..., description="A list of goals to achieve for this swarm.")
    additional_info:str = Field(..., description="Additional relevant information")
    
    async def run(self):
        directive = f"""Goals: \n {self.goals} \n\n Additional Info: {self.additional_info}"""
        return directive

class SiteScraper(OpenAISchema):
    """
    Retrieves all the text content from a site and returns specific context based on what the swarm is looking for. 
    """
    url: str = Field(..., description="URL of the site to scrape.")
    
    imp:str = Field(..., description="Information on what the swarm is looking for")

    async def run(self)->str:

        response = requests.get(self.url)

        # If the request was successful (status code 200)
        if response.status_code == 200:
            # Get the content of the response
            page_content = response.content

            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(page_content, 'html.parser')

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = preprocess('\n'.join(chunk for chunk in chunks if chunk))
        words = text.split(" ")
        if len(words) > 14000:
            text = " ".join([words[i] for i in range(14000)])
            
        
        return text
