from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL :str 
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    redis_host: str = "localhost"
    redis_port: int = 6379,
    jti_expiry: int = 3000
    roles:list[str]
    allowed_hosts:list[str]
    rate_limts: str = "15/minute"

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra= "ignore"
    )


Config = Settings()
