"""PostgreSQL connection settings loaded from environment variables."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str

    @classmethod
    def from_environment(cls) -> "DatabaseConfig":
        load_dotenv(Path(__file__).with_name(".env"))
        required = ("DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD")
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            raise ValueError(
                "Missing database environment variable(s): " + ", ".join(missing)
            )
        try:
            port = int(os.getenv("DB_PORT", "5432"))
        except ValueError as error:
            raise ValueError("DB_PORT must be an integer.") from error
        if not 1 <= port <= 65535:
            raise ValueError("DB_PORT must be between 1 and 65535.")

        return cls(
            host=os.environ["DB_HOST"],
            port=port,
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )
