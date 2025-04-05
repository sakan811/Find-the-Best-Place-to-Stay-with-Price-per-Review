# Stage 1: Build environment
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory for the build stage
WORKDIR /build

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN uv pip install --system -r requirements.txt

# Stage 2: Production environment
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble AS production
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.*/site-packages /usr/local/lib/python3.*/site-packages/

# Copy only necessary application files
COPY extract_booking_headers.py logging_config.py __init__.py ./

# Set PATH to include user-specific bin directory
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Install playwright binaries
RUN pip install playwright

# Command to run when container starts
CMD ["python", "extract_booking_headers.py"]