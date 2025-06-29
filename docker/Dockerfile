# Dockerfile (Using the recommended pipx method)

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 1. Install pipx, a tool for installing and running Python applications in isolated environments.
RUN pip install pipx

# 2. Ensure the directory for pipx-installed applications is in the system's PATH.
RUN pipx ensurepath

# 3. Explicitly add the standard pipx bin directory to the PATH for subsequent commands.
ENV PATH="/root/.local/bin:$PATH"

# 4. Use pipx to install poetry. This automatically handles its environment and path.
RUN pipx install poetry

# Set the working directory
WORKDIR /app

# Copy dependency files
COPY poetry.lock pyproject.toml /app/

# Now 'poetry' is a known command, so we can use it directly.
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --with deployment --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=tests.settings

# Gunicorn was installed system-wide by the poetry install command, so we can call it directly.
CMD ["gunicorn", "tests.wsgi:application", "--bind", "0.0.0.0:8000"]