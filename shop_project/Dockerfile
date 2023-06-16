FROM python:3.11.1
LABEL authors="emmel"
ENV PYTHONBUFFERED 1
ENV POETRY_VERSION 1.3.2
RUN pip install --upgrade pip
RUN pip install "poetry==${POETRY_VERSION}"
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --without test --no-root
COPY . /app
