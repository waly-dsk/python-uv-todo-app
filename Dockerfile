FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project --no-dev

COPY src/ ./src/
COPY main.py ./
COPY README.md ./

RUN uv sync --no-dev

FROM python:3.12-slim AS final
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/main.py /app/main.py

EXPOSE 8000
CMD ["/app/.venv/bin/python", "main.py"]
