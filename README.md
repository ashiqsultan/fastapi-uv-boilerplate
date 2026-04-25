# Fast API UV Docker Boilerplate

A boilerplate code to initiate new projects with FastAPI

## Whats included
- UV package manager.
- Docker compose.
- Logger
- pydantic_settings for reading env
- Ruff Linter

## How to start
- Create a .env file
- Add a variable `ENVIRONMENT=development`
- `docker compose up`

- Go to `http://localhost:8008/docs`

## How to Lint and Format
- `uv run ruff check`
- `uv run ruff format`

