FROM python:3.11.9-bullseye
WORKDIR /online_cinema

ENV PYTHONPATH "${PYTHONPATH}:."

COPY . .

RUN python -m pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install -vvv --no-root \
    && poetry update
