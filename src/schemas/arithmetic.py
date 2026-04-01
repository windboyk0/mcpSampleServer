from pydantic import BaseModel


class ArithmeticInput(BaseModel):
    a: float
    b: float


class ArithmeticOutput(BaseModel):
    result: float
    expression: str
