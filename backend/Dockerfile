FROM python:3.13.0-alpine3.20
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies as root
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Set PATH to include user-specific bin directory
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application as the non-root user
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]