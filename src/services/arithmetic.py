from schemas.arithmetic import ArithmeticInput, ArithmeticOutput


class ArithmeticService:
    def add(self, inp: ArithmeticInput) -> ArithmeticOutput:
        return ArithmeticOutput(
            result=inp.a + inp.b,
            expression=f"{inp.a} + {inp.b}",
        )

    def subtract(self, inp: ArithmeticInput) -> ArithmeticOutput:
        return ArithmeticOutput(
            result=inp.a - inp.b,
            expression=f"{inp.a} - {inp.b}",
        )

    def multiply(self, inp: ArithmeticInput) -> ArithmeticOutput:
        return ArithmeticOutput(
            result=inp.a * inp.b,
            expression=f"{inp.a} × {inp.b}",
        )

    def divide(self, inp: ArithmeticInput) -> ArithmeticOutput:
        if inp.b == 0:
            raise ValueError("나누는 수(b)가 0입니다. 0으로 나눌 수 없습니다.")
        return ArithmeticOutput(
            result=inp.a / inp.b,
            expression=f"{inp.a} ÷ {inp.b}",
        )
