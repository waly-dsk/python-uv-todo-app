FROM python:3.12-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project --no-dev

COPY src/ ./src/
COPY main.py ./
COPY db.py ./
COPY static/ ./static/
COPY README.md ./
COPY todo.db ./

RUN uv sync --no-dev


FROM python:3.12-alpine AS final

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/db.py /app/db.py
COPY --from=builder /app/static /app/static
COPY --from=builder /app/todo.db /app/todo.db

EXPOSE 8000

CMD ["/app/.venv/bin/python", "main.py"]
