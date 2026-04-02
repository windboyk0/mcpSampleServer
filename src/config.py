from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    server_name: str = "arithmetic-mcp"  # .env: SERVER_NAME
    # api_key: str = ""                 # .env: API_KEY — ApiKeyMiddleware 사용 시 주석 해제


settings = Settings()
