FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project --no-dev

COPY src/ ./src/
COPY main.py ./
COPY README.md ./

RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "python", "main.py"]
