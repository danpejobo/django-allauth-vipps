# Dockerfile (Improved Version)

FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pipx, the recommended tool for installing Python applications like Poetry
RUN pip install pipx
RUN pipx ensurepath

# Add the pipx path to the system PATH. This is where Poetry will live.
ENV PATH="/root/.local/bin:$PATH"

# Install Poetry using pipx
RUN pipx install poetry

WORKDIR /app

# Copy only the dependency files to leverage Docker's build cache
COPY poetry.lock pyproject.toml /app/

# Tell Poetry to install dependencies into the main system environment, not a virtual one.
# This makes the executable (like gunicorn) available system-wide in the container.
# Install main dependencies AND the 'deployment' group dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --with deployment --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

EXPOSE 8000

# Since we installed to the system, we can now call gunicorn directly.
# This is simpler and less prone to path issues.
CMD ["gunicorn", "tests.wsgi:application", "--bind", "0.0.0.0:8000", "--settings=tests.settings"]