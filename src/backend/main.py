from swarmtypes import *
from context import Schema
from fastapi import FastAPI, Response, Request
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import uuid

from utils import create_communication_schema



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List your frontend origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/upload-agent-data/")
async def upload_agent_data(new_data: AgentData):
    try:
        # Load existing data
        try:
            with open("JsonFiles/agent_data.json", "r") as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            data = []

        new_data.agentID = str(uuid.uuid4())

        data.append(new_data.model_dump())

        # Write updated data back to file
        with open("JsonFiles/agent_data.json", "w") as f:
            f.write(json.dumps(data, indent=4))

        return {"message": "Data updated successfully", "content":new_data.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-agent-data/")
async def get_agent_data():
    try:
        with open("JsonFiles/agent_lib.json", "r") as file:
            data = json.loads(file.read())
        
        for agent in data:
            agent['agentID'] =  str(uuid.uuid4())
            
        print(data)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload-swarm-data/")
async def upload_swarm_data(graphdata:GraphData):
    
    try:
        schema, user = create_communication_schema(graphdata)
        schema.viz()
        await schema.system_pass(message="", starting_node=user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    

