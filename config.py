from pydantic import BaseSettings


class Settings(BaseSettings):
    deta_project_key: str


settings = Settings()
