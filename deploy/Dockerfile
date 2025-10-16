FROM python:3.11-slim AS backend

WORKDIR /app

COPY backend/pyproject.toml backend/poetry.lock* backend/alembic.ini /app/

COPY deploy/configs /app/deploy/configs 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY backend/src /app/src

CMD ["uvicorn", "src.main.web:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

