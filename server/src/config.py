import os


class Config:
    @property
    def DB_CONFIG(self) -> str:
        user = os.getenv("DATABASE__USERNAME", "fastapi")
        password = os.getenv("DATABASE__PASSWORD", "fastapi-password")
        host = os.getenv("DATABASE__HOSTNAME", "localhost")
        port = os.getenv("DATABASE__PORT", "5432")
        db = os.getenv("DATABASE__DB", "fastapi")

        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"


config = Config()
