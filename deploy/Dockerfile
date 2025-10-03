FROM python:3.11-slim AS backend

WORKDIR /app

COPY pyproject.toml poetry.lock* alembic.ini /app/

COPY deploy/configs /app/deploy/configs 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY backend /app/backend

CMD ["uvicorn", "backend.main.web:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

