# CLAUDE.md

이 파일은 Claude Code가 이 프로젝트에서 코드를 생성·수정할 때 따르는 행동 규칙이다.
코드 작성 전 반드시 이 파일을 먼저 읽는다.

---

## 프로젝트 개요

**사칙연산 MCP 서버** — 덧셈·뺄셈·곱셈·나눗셈 네 가지 연산을 Claude에게 제공하는 MCP 서버.

---

## 스택

- Python 3.11+
- `mcp[cli]` — 공식 MCP Python SDK (FastMCP 사용)
- `pydantic` v2 — 입력 스키마 및 설정
- `pydantic-settings` — 환경변수 관리
- `pytest` + `pytest-asyncio` — 테스트
- `ruff` — 포맷 및 린트

---

## 프로젝트 구조

파일을 새로 만들 때 반드시 아래 위치에 만든다.

```
src/
  server.py              # 진입점: FastMCP 초기화 및 핸들러 등록
  config.py              # Settings 클래스 (환경변수 전용)
  tools/
    __init__.py          # register_all_tools(mcp) 노출
    arithmetic.py        # 사칙연산 Tool 핸들러
  resources/
    __init__.py          # register_all_resources(mcp) 노출
  prompts/
    __init__.py          # register_all_prompts(mcp) 노출
  schemas/
    arithmetic.py        # Pydantic 입출력 모델 (AddInput, SubtractInput, ...)
  services/
    arithmetic.py        # 비즈니스 로직 — 순수 계산 함수
tests/
  unit/
    test_arithmetic_service.py    # services/ 단위 테스트
  integration/
    test_arithmetic_tool.py       # tools/ 통합 테스트
.env                 # 실제 환경변수 값 (git 제외, 로컬 전용)
.env.example         # 환경변수 키 목록 및 예시값 (git 포함, 팀 공유용)
pyproject.toml       # 프로젝트 메타데이터, 의존성, 빌드·테스트·린트 설정
```

---

## 제공 Tool 목록

| Tool 이름    | 설명                              | 입력           | 반환  |
|-------------|----------------------------------|----------------|-------|
| `add`       | 두 수를 더한다                    | a: float, b: float | str (JSON) |
| `subtract`  | 두 수를 뺀다 (a − b)              | a: float, b: float | str (JSON) |
| `multiply`  | 두 수를 곱한다                    | a: float, b: float | str (JSON) |
| `divide`    | 두 수를 나눈다 (a ÷ b)            | a: float, b: float | str (JSON) |

> `divide` 는 b == 0 일 때 반드시 명확한 오류 메시지를 반환한다.

---

## 코딩 규칙

### 타입
- 모든 함수에 타입 힌트 필수
- `Any` 타입 사용 금지
- Pydantic 모델 파싱은 `model_validate()` 사용 (`**dict` 언패킹 금지)

### 비동기
- 외부 I/O는 반드시 `async/await` 사용
- 동기 블로킹 함수(`open` 등)는 `asyncio.to_thread()` 경유
- 사칙연산 서비스 자체는 순수 동기 함수로 작성 (`async` 불필요)

### 환경변수
- 환경변수는 `config.py`의 `Settings` 클래스를 통해서만 읽는다
- 코드 안에 비밀값 하드코딩 금지

### 오류 처리
- `except Exception: pass` 묵음 처리 금지
- 오류 메시지는 Claude가 다음 행동을 결정할 수 있을 만큼 구체적으로 작성
- 예상 외 오류의 스택 트레이스는 `sys.stderr`에만 출력

### 절대 금지
- `print()` 사용 금지 — stdio transport 오염으로 서버가 죽는다. 디버그 출력은 반드시 `sys.stderr`에만 한다
- Service 레이어에서 외부 I/O 직접 호출 금지 (Infra 레이어 경유)
- Tool 하나에 두 가지 이상의 책임 금지

---

## 레이어 책임

| 레이어 | 하는 일 | 하지 않는 일 |
|--------|---------|------------|
| `tools/` | 입력 파싱, 오류 래핑, Service 호출 | 비즈니스 로직 |
| `services/` | 비즈니스 로직, 순수 함수 | 외부 I/O 직접 호출 |
| `infra/` | 외부 API·DB·파일 I/O | 비즈니스 규칙 |

---

## 구현 패턴

### config.py

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    # 필요한 환경변수를 여기에 추가
    # server_name: str = "arithmetic-mcp"
```

### server.py

```python
from mcp.server.fastmcp import FastMCP
from tools import register_all_tools
from resources import register_all_resources
from prompts import register_all_prompts

mcp = FastMCP(name="arithmetic-mcp")
register_all_tools(mcp)
register_all_resources(mcp)
register_all_prompts(mcp)

if __name__ == "__main__":
    mcp.run()
```

### schemas/arithmetic.py (예시)

```python
from pydantic import BaseModel

class ArithmeticInput(BaseModel):
    a: float
    b: float

class ArithmeticOutput(BaseModel):
    result: float
    expression: str
```

### services/arithmetic.py (예시)

```python
from schemas.arithmetic import ArithmeticInput, ArithmeticOutput

class ArithmeticService:
    def add(self, inp: ArithmeticInput) -> ArithmeticOutput:
        return ArithmeticOutput(result=inp.a + inp.b, expression=f"{inp.a} + {inp.b}")

    def subtract(self, inp: ArithmeticInput) -> ArithmeticOutput:
        return ArithmeticOutput(result=inp.a - inp.b, expression=f"{inp.a} - {inp.b}")

    def multiply(self, inp: ArithmeticInput) -> ArithmeticOutput:
        return ArithmeticOutput(result=inp.a * inp.b, expression=f"{inp.a} × {inp.b}")

    def divide(self, inp: ArithmeticInput) -> ArithmeticOutput:
        if inp.b == 0:
            raise ValueError("나누는 수(b)가 0입니다. 0으로 나눌 수 없습니다.")
        return ArithmeticOutput(result=inp.a / inp.b, expression=f"{inp.a} ÷ {inp.b}")
```

### tools/arithmetic.py (예시)

```python
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

    # subtract / multiply / divide 도 동일한 패턴으로 작성
```

---

## 새 Tool 추가 순서

아래 순서를 반드시 지킨다. 건너뛰지 않는다.

1. `schemas/arithmetic.py` — Pydantic 입출력 모델 정의 또는 수정
2. `services/arithmetic.py` — 비즈니스 로직 구현
3. `infra/[이름].py` — 외부 연동 필요 시 작성 (사칙연산은 불필요)
4. `tools/arithmetic.py` — Tool 핸들러 작성
5. `tools/__init__.py` — `register_all_tools()`에 등록
6. `tests/unit/test_arithmetic_service.py` — Service 단위 테스트
7. `tests/integration/test_arithmetic_tool.py` — Tool 통합 테스트

---

## 테스트 규칙

- 외부 의존성은 `AsyncMock`으로 교체
- 테스트마다 정상 케이스 + 오류 케이스 각각 작성
- `divide` 는 반드시 0 나눗셈 오류 케이스를 포함한다

---

## 실행 방법

```bash
# 가상환경 설정
cd d:/VS-Workspace/claude-workspace/mcpSampleServer
python -m venv venv 2>&1
venv\Scripts\activate

# 의존성 설치
pip install -e ".[dev]"

# MCP 서버 실행 (stdio)
python src/server.py

# 테스트 실행
pytest tests/ -v
```
