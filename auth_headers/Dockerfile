FROM mcr.microsoft.com/playwright/python:v1.51.0-noble
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app

# Set the working directory
WORKDIR /app

RUN uv sync --frozen

# Install dependencies
RUN uv add playwright Flask gunicorn

ENV PATH="/app/.venv/bin:$PATH"

# Use Gunicorn to run the application with WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:4000", "app:app"]