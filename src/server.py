from mcp.server.fastmcp import FastMCP

from config import settings
from prompts import register_all_prompts
from resources import register_all_resources
from tools import register_all_tools

mcp = FastMCP(name=settings.server_name)
register_all_tools(mcp)
register_all_resources(mcp)
register_all_prompts(mcp)

if __name__ == "__main__":
    mcp.run()
