FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.5 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY . .

RUN apt-get update \
    && apt-get install -y \
        curl \
        build-essential \
        libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3.13 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

EXPOSE 8030

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8030"]
