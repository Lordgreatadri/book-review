from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    domain_name:str
    DATABASE_URL :str 
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    salt: str = "book-review-api-secret"
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    redis_host: str = "localhost"
    redis_port: int = 6379,
    jti_expiry: int = 3000
    roles:list[str]
    allowed_hosts:list[str]
    rate_limts: str = "15/minute"
    mail_username: str
    mail_password: str
    mail_from_email :str
    mail_port: int
    mail_host: str
    mail_from_name: str
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    mail_use_credentials: bool = True
    mail_validate_certs: bool = True


    model_config = SettingsConfigDict(
        env_file = ".env",
        extra= "ignore"
    )


Config = Settings()
