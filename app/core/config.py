from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"

    database_url: str
    cache_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    token_type_hint: str = "Bearer"
    access_token_expire_seconds: int = 15 * 60
    refresh_token_expire_seconds: int = 7 * 24 * 60 * 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def is_environment(self, environment_name: str) -> bool:
        return self.app_env.casefold() == environment_name.casefold()

    def is_development(self) -> bool:
        return self.is_environment("DEVELOPMENT")

    def is_testing(self) -> bool:
        return self.is_environment("TESTING")

    def is_production(self) -> bool:
        return self.is_environment("PRODUCTION")


settings = Settings()
