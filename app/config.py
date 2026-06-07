from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    #设置默认值
    app_name: str = "TestPilot"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./testpilot.db"
    model_config = {"env_file":".env","env_file_encoding": "utf-8"}

settings = Settings()