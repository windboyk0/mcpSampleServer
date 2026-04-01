import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

import pytest
from unittest.mock import MagicMock
from schemas.arithmetic import ArithmeticOutput
from services.arithmetic import ArithmeticService
from tools.arithmetic import register_arithmetic_tools


def _make_mock_service() -> MagicMock:
    mock = MagicMock(spec=ArithmeticService)
    mock.add.return_value = ArithmeticOutput(result=5.0, expression="3.0 + 2.0")
    mock.subtract.return_value = ArithmeticOutput(result=1.0, expression="3.0 - 2.0")
    mock.multiply.return_value = ArithmeticOutput(result=6.0, expression="3.0 × 2.0")
    mock.divide.return_value = ArithmeticOutput(result=1.5, expression="3.0 ÷ 2.0")
    return mock


class TestAddTool:
    @pytest.mark.asyncio
    async def test_add_returns_json(self) -> None:
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP(name="test")
        register_arithmetic_tools(mcp)

        tool_fn = None
        for tool in mcp._tool_manager._tools.values():
            if tool.name == "add":
                tool_fn = tool.fn
                break

        assert tool_fn is not None
        result_json = await tool_fn(a=3.0, b=2.0)
        data = json.loads(result_json)
        assert data["result"] == 5.0
        assert "+" in data["expression"]

    @pytest.mark.asyncio
    async def test_subtract_returns_json(self) -> None:
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP(name="test")
        register_arithmetic_tools(mcp)

        tool_fn = None
        for tool in mcp._tool_manager._tools.values():
            if tool.name == "subtract":
                tool_fn = tool.fn
                break

        assert tool_fn is not None
        result_json = await tool_fn(a=10.0, b=3.0)
        data = json.loads(result_json)
        assert data["result"] == 7.0

    @pytest.mark.asyncio
    async def test_multiply_returns_json(self) -> None:
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP(name="test")
        register_arithmetic_tools(mcp)

        tool_fn = None
        for tool in mcp._tool_manager._tools.values():
            if tool.name == "multiply":
                tool_fn = tool.fn
                break

        assert tool_fn is not None
        result_json = await tool_fn(a=4.0, b=3.0)
        data = json.loads(result_json)
        assert data["result"] == 12.0

    @pytest.mark.asyncio
    async def test_divide_normal(self) -> None:
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP(name="test")
        register_arithmetic_tools(mcp)

        tool_fn = None
        for tool in mcp._tool_manager._tools.values():
            if tool.name == "divide":
                tool_fn = tool.fn
                break

        assert tool_fn is not None
        result_json = await tool_fn(a=10.0, b=4.0)
        data = json.loads(result_json)
        assert data["result"] == 2.5

    @pytest.mark.asyncio
    async def test_divide_by_zero_returns_error_message(self) -> None:
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP(name="test")
        register_arithmetic_tools(mcp)

        tool_fn = None
        for tool in mcp._tool_manager._tools.values():
            if tool.name == "divide":
                tool_fn = tool.fn
                break

        assert tool_fn is not None
        result = await tool_fn(a=5.0, b=0.0)
        assert "0으로 나눌 수 없습니다" in result
