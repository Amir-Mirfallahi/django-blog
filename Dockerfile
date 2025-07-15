FROM python:3.13-slim-buster

# Installing uv dependency manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Settings up the workdir
WORKDIR /app

# Copying crucial dependencies
COPY pyproject.toml /app/
COPY .python-version /app/
COPY 5.2 /app/
COPY uv.lock /app/

RUN uv sync --locked

COPY ./core /app/