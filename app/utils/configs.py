import sqlalchemy
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_DRIVER: str = "postgresql+asyncpg"
    TOKEN_API: str
    ALLOW_DOC: bool = True
    DB_LOG: bool = False
    LIST_CORS: list[str] = ['*']
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE: int = 30
    TOKEN_REFRESH_EXPIRE: int = 2880

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_db_url(self, to_string=False):
        url = sqlalchemy.engine.url.URL.create(drivername=self.DB_DRIVER, username=self.DB_USER,
                                               password=self.DB_PASSWORD, host=self.DB_HOST, port=self.DB_PORT,
                                               database=self.DB_NAME)
        if to_string:
            url = url.render_as_string(hide_password=False).replace('%', '%%')
        return url


project_settings = Settings()
