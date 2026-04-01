import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

import pytest
from schemas.arithmetic import ArithmeticInput
from services.arithmetic import ArithmeticService


@pytest.fixture
def service() -> ArithmeticService:
    return ArithmeticService()


class TestAdd:
    def test_add_positive(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": 3.0, "b": 2.0})
        out = service.add(inp)
        assert out.result == 5.0
        assert out.expression == "3.0 + 2.0"

    def test_add_negative(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": -1.0, "b": -4.0})
        out = service.add(inp)
        assert out.result == -5.0


class TestSubtract:
    def test_subtract_normal(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": 10.0, "b": 3.0})
        out = service.subtract(inp)
        assert out.result == 7.0
        assert out.expression == "10.0 - 3.0"

    def test_subtract_negative_result(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": 2.0, "b": 5.0})
        out = service.subtract(inp)
        assert out.result == -3.0


class TestMultiply:
    def test_multiply_normal(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": 4.0, "b": 3.0})
        out = service.multiply(inp)
        assert out.result == 12.0
        assert "×" in out.expression

    def test_multiply_by_zero(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": 99.0, "b": 0.0})
        out = service.multiply(inp)
        assert out.result == 0.0


class TestDivide:
    def test_divide_normal(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": 10.0, "b": 4.0})
        out = service.divide(inp)
        assert out.result == 2.5
        assert "÷" in out.expression

    def test_divide_by_zero_raises(self, service: ArithmeticService) -> None:
        inp = ArithmeticInput.model_validate({"a": 5.0, "b": 0.0})
        with pytest.raises(ValueError, match="0으로 나눌 수 없습니다"):
            service.divide(inp)
