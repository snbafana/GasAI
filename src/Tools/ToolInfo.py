from . import ToolForge
from instructor import OpenAISchema

tools = [(name, cls) for name, cls in ToolForge.__dict__.items() if isinstance(cls, type) and issubclass(cls, OpenAISchema)]
tools.pop(0)
ToolNameDict = dict(tools)

