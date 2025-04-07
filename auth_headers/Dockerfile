# Stage 1: Build environment
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory for the build stage
WORKDIR /build

# Copy only the requirements file first to leverage Docker cache
COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync

# Stage 2: Production environment
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble AS production
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.*/site-packages /usr/local/lib/python3.*/site-packages/

# Copy necessary application files
COPY . .

# Set PATH to include user-specific bin directory
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Install dependencies
RUN pip install playwright Flask gunicorn

# Use Gunicorn to run the application with WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:4000", "app:app"]