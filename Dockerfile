FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (no project, just deps)
RUN uv sync --frozen --no-install-project

# Copy the rest of the project
COPY . .

# Install the project itself
RUN uv sync --frozen

EXPOSE 8008

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8008"]