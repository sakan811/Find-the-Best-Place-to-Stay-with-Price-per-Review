FROM python:3.12 as backend

WORKDIR /app/backend

# Copy only the backend files
COPY /backend /app/backend

# Create and activate virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

FROM node:21 as frontend

# Copy only the frontend files
COPY /frontend /app/frontend

FROM python:3.12 as final

# Copy backend files
COPY --from=backend /app /app

# Copy frontend files
COPY --from=frontend /app/frontend /app/frontend

# Set up environment
ENV PATH="/app/venv/bin:$PATH"
WORKDIR /app/backend

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]