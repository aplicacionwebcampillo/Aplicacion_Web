from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    database_name_test: str = Field(..., env="DATABASE_NAME_TEST")

    class Config:
        env_file = ".env"

settings = Settings()
