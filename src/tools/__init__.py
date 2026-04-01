from mcp.server.fastmcp import FastMCP

from tools.arithmetic import register_arithmetic_tools


def register_all_tools(mcp: FastMCP) -> None:
    register_arithmetic_tools(mcp)
