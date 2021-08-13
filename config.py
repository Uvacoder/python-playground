from pydantic import BaseSettings


class Settings(BaseSettings):
    deta_project_key: str
    jwt_key: str


settings = Settings()
