import sys

from mcp.server.fastmcp import FastMCP

from schemas.arithmetic import ArithmeticInput
from services.arithmetic import ArithmeticService


def register_arithmetic_tools(mcp: FastMCP) -> None:
    service = ArithmeticService()

    @mcp.tool(
        name="add",
        description=(
            "두 수를 더한다. "
            "덧셈, 합산, 더하기 요청에 호출한다. "
            "결과값과 수식 문자열을 JSON으로 반환한다."
        ),
    )
    async def add(a: float, b: float) -> str:
        inp = ArithmeticInput.model_validate({"a": a, "b": b})
        result = service.add(inp)
        return result.model_dump_json(indent=2)

    @mcp.tool(
        name="subtract",
        description=(
            "두 수를 뺀다 (a − b). "
            "빼기, 차이, 감산 요청에 호출한다. "
            "결과값과 수식 문자열을 JSON으로 반환한다."
        ),
    )
    async def subtract(a: float, b: float) -> str:
        inp = ArithmeticInput.model_validate({"a": a, "b": b})
        result = service.subtract(inp)
        return result.model_dump_json(indent=2)

    @mcp.tool(
        name="multiply",
        description=(
            "두 수를 곱한다. "
            "곱셈, 배수, 곱하기 요청에 호출한다. "
            "결과값과 수식 문자열을 JSON으로 반환한다."
        ),
    )
    async def multiply(a: float, b: float) -> str:
        inp = ArithmeticInput.model_validate({"a": a, "b": b})
        result = service.multiply(inp)
        return result.model_dump_json(indent=2)

    @mcp.tool(
        name="divide",
        description=(
            "두 수를 나눈다 (a ÷ b). "
            "나눗셈, 몫, 나누기 요청에 호출한다. "
            "b가 0이면 오류 메시지를 반환한다. "
            "결과값과 수식 문자열을 JSON으로 반환한다."
        ),
    )
    async def divide(a: float, b: float) -> str:
        inp = ArithmeticInput.model_validate({"a": a, "b": b})
        try:
            result = service.divide(inp)
        except ValueError as e:
            print(f"divide error: b={b}, reason={e}", file=sys.stderr)
            return str(e)
        return result.model_dump_json(indent=2)
