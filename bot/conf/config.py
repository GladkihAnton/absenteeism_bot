from pydantic import BaseSettings


class Settings(BaseSettings):
    ASYNC_DATABASE_URL: str
    BOT_TOKEN: str


settings = Settings()
