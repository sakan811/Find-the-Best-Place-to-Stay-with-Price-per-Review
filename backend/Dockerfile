FROM python:3.12-alpine

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
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY --chown=appuser:appgroup . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application as the non-root user
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]