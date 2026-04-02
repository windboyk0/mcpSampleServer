from mcp.server.fastmcp import FastMCP

from config import settings
from prompts import register_all_prompts
from resources import register_all_resources
from tools import register_all_tools


# [API Key 인증 미들웨어]
# - .env 의 API_KEY 값이 설정된 경우에만 인증 활성화
# - 클라이언트는 모든 요청 헤더에 아래 형식으로 키를 전달해야 함
#   Authorization: Bearer <API_KEY>
# - API_KEY 가 비어있으면 인증 없이 동작 (로컬 개발 시 편의)
# - 주의: Claude Desktop 은 커스텀 헤더 전송을 지원하지 않아
#         Claude Desktop 연결 목적으로는 실질적인 효과가 없음
#         MCP 표준 인증은 OAuth 2.0 사용 권장
# import sys
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import JSONResponse
#
# class ApiKeyMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if settings.api_key:
#             auth_header = request.headers.get("Authorization", "")
#             if auth_header != f"Bearer {settings.api_key}":
#                 print(
#                     f"Unauthorized request from {request.client}",
#                     file=sys.stderr,
#                 )
#                 return JSONResponse(
#                     {"error": "Unauthorized: invalid or missing API key"},
#                     status_code=401,
#                 )
#         return await call_next(request)


mcp = FastMCP(name=settings.server_name)
register_all_tools(mcp)
register_all_resources(mcp)
register_all_prompts(mcp)

if __name__ == "__main__":
    # [STDIO 방식] Claude Desktop 로컬 연결 — command/args 방식으로 등록
    mcp.run()

    # [Streamable HTTP 방식] HTTP 서버로 실행
    # 로컬:       http://localhost:8000/mcp
    # Codespaces: https://<codespace-name>-8000.app.github.dev/mcp
    # mcp = FastMCP(name=settings.server_name, host="0.0.0.0", port=8000)
    # mcp.streamable_http_app().add_middleware(ApiKeyMiddleware)  # API Key 사용 시 주석 해제
    # mcp.run(transport="streamable-http")

    # [SSE 방식]
    # 로컬:       http://localhost:8000/sse
    # Codespaces: https://<codespace-name>-8000.app.github.dev/sse
    # mcp = FastMCP(name=settings.server_name, host="0.0.0.0", port=8000)
    # mcp.run(transport="sse")
