FROM python:3.12.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /payment_service

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /payment_service/
RUN poetry install --no-interaction
RUN poetry add uwsgi
# на винде uwsgi нельзя установить

COPY . /payment_service/