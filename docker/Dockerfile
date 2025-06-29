# Dockerfile using the official curl installer

FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 1. Install Poetry using the official installer script from the documentation
RUN curl -sSL https://install.python-poetry.org | python3 -

# 2. Add the directory where the installer places the 'poetry' command to the system's PATH.
#    Inside the container (as the root user), this is /root/.local/bin.
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY poetry.lock pyproject.toml /app/

# Configure Poetry and install project dependencies (including the 'deployment' group for gunicorn)
RUN poetry config virtualenvs.create false && poetry install --no-root --with deployment --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

EXPOSE 8000

# Set the DJANGO_SETTINGS_MODULE environment variable for Gunicorn to use.
ENV DJANGO_SETTINGS_MODULE=tests.settings

# The CMD remains the same. Gunicorn was installed system-wide, so it can be called directly.
CMD ["gunicorn", "tests.wsgi:application", "--bind", "0.0.0.0:8000"]