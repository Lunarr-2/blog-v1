from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    algorithm : str = "HS256"
    access_token_expire_minutes : int = 30
    secret_key : SecretStr
    imagekit_private_key : SecretStr
    imagekit_public_key: SecretStr
    image_url_endpoint: SecretStr


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding= "utf-8"

    )


settings = Settings()