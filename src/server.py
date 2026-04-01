from mcp.server.fastmcp import FastMCP

from config import settings
from prompts import register_all_prompts
from resources import register_all_resources
from tools import register_all_tools

mcp = FastMCP(name=settings.server_name, host="0.0.0.0", port=8000)
register_all_tools(mcp)
register_all_resources(mcp)
register_all_prompts(mcp)

if __name__ == "__main__":
    # [STDIO 방식] Claude Desktop 로컬 연결 시 사용
    # claude_desktop_config.json 에 command/args 로 등록
    # mcp.run()

    # [Streamable HTTP 방식] HTTP 서버로 실행
    # 로컬:       http://localhost:8000/mcp
    # Codespaces: https://<codespace-name>-8000.app.github.dev/mcp
    # mcp.run(transport="streamable-http")

    # [SSE 방식] Claude Desktop 원격 연결 시 사용
    # 로컬:       http://localhost:8000/sse
    # Codespaces: https://<codespace-name>-8000.app.github.dev/sse
    mcp.run(transport="sse")
