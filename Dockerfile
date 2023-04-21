FROM python:3.10.5-bullseye
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:."

COPY . .

RUN python -m pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install -vvv --no-root \
    && poetry update
