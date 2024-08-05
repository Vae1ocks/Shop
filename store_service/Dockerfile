FROM python:3.12.0

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /store_service

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /store_service/
RUN poetry install --no-interaction

COPY . /store_service/