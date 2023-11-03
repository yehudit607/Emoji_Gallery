from pydantic import BaseSettings


class Settings(BaseSettings):
    # DB
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
