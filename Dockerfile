FROM mcr.microsoft.com/playwright/python:v1.62.0-noble
RUN pip install uv --break-system-packages
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync
COPY . .
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"]