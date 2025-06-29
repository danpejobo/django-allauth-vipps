# Dockerfile using the official curl installer

FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 1. Install Poetry using the official installer script from the documentation
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY poetry.lock pyproject.toml /app/

# Call poetry using its full, absolute path to avoid any PATH issues.
RUN /root/.local/share/pypoetry/venv/bin/poetry config virtualenvs.create false && \
    /root/.local/share/pypoetry/venv/bin/poetry install --no-root --with deployment --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

EXPOSE 8000

# Set the DJANGO_SETTINGS_MODULE environment variable for Gunicorn to use.
ENV DJANGO_SETTINGS_MODULE=tests.settings

# The CMD remains the same. Gunicorn was installed system-wide, so it can be called directly.
CMD ["gunicorn", "tests.wsgi:application", "--bind", "0.0.0.0:8000"]