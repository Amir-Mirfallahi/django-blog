FROM python:3.13-alpine

# Installing uv dependency manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Settings up the workdir
WORKDIR /app

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock .python-version /app

# Install dependencies
RUN uv sync --locked

# Copy application code
COPY ./core /app/core
