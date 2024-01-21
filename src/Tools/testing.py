import ToolForge

print(dict([(name, cls) for name, cls in ToolForge.__dict__.items() if isinstance(cls, type)]))