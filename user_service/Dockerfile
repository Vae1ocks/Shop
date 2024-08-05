FROM python:3.12.0

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /user_service

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /user_service/
RUN poetry install --no-interaction

COPY . /user_service/

