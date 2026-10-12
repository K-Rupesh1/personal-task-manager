# Personal Task Manager

This project uses `uv` for dependency management and environment creation.

## Setup

```sh
uv sync
```

Activate the project environment in the shell you are using:

```sh
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows cmd.exe
.venv\Scripts\activate.bat
```

`uv sync` reads dependencies from `pyproject.toml`, resolves them, and installs them with the lockfile in `uv.lock`.

## Run

```sh
uv run python main.py
```

For the FastAPI application, use:

```sh
uv run uvicorn app.main:app --reload
```

## Dependency updates

Add or update packages with uv:

```sh
uv add fastapi psycopg2
uv lock
```

Do not use `pip` or the legacy requirements files in this project. The `pyproject.toml` and `uv.lock` files are the single source of truth for dependencies.
