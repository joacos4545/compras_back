"""Aplica las migraciones y arranca la API para desarrollo local."""

import os
from pathlib import Path

import uvicorn
from alembic import command
from alembic.config import Config


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    os.chdir(project_dir)
    command.upgrade(Config(str(project_dir / "alembic.ini")), "head")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()


