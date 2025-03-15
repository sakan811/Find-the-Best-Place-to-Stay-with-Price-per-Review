FROM python:3.13-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user and group
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -S appuser

# Set the working directory and ensure it's owned by the non-root user
WORKDIR /app
RUN chown appuser:appgroup /app

# Switch to the non-root user for the rest of the build stage
USER appuser

# Set PATH to include user-specific bin directory
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the requirements file and install dependencies
COPY --chown=appuser:appgroup requirements.txt ./
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Install playwright
RUN playwright install --with-deps

# Copy the rest of the application code
COPY --chown=appuser:appgroup . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application as the non-root user
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]