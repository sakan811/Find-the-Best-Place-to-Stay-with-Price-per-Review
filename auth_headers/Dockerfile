FROM mcr.microsoft.com/playwright/python:v1.50.0-noble
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user and group
RUN getent group 2000 || groupadd -g 2000 appgroup && \
    getent passwd 2000 || useradd -u 2000 -g 2000 -s /bin/bash -m appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies as root
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Set ownership of the application directory to the non-root user
RUN chown -R 2000:2000 /app

# Switch to the non-root user for the rest of the build stage
USER 2000:2000

# Set PATH to include user-specific bin directory
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the rest of the application code with proper ownership
COPY --chown=2000:2000 . .