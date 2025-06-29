# Dockerfile

# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installer Poetry
ENV POETRY_VERSION=1.7.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependency files first to leverage Docker's build cache
COPY poetry.lock pyproject.toml /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application using Gunicorn
CMD ["poetry", "run", "gunicorn", "tests.wsgi:application", "--bind", "0.0.0.0:8000", "--settings=tests.settings"]