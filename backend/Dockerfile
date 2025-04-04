FROM python:3.13.0-alpine3.20
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user and group
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -S appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies as root
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Set ownership of the application directory to the non-root user
RUN chown -R 1000:1000 /app

# Switch to the non-root user for the rest of the build stage
USER 1000:1000

# Set PATH to include user-specific bin directory
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the rest of the application code with proper ownership
COPY --chown=1000:1000 . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application as the non-root user
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]