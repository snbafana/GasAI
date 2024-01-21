from pydantic import BaseModel
from typing import Union, List, Dict, Any

from typing import List, Optional
from pydantic import BaseModel

class Position(BaseModel):
    x: float
    y: float

class AgentData(BaseModel):
    agentID: str
    agentName: str
    agentInstruction: str
    agentDescription: str
    agentTools: List[str]

class Node(BaseModel):
    id: str
    type: str
    data: AgentData
    position: Position
    width: int
    height: int
    selected: Optional[bool] = None
    positionAbsolute: Optional[Position] = None
    dragging: Optional[bool]  = None

class Edge(BaseModel):
    source: str
    target: str
    id: str
    markerEnd: dict
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class Viewport(BaseModel):
    x: float
    y: float
    zoom: float

class GraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    viewport: Viewport
