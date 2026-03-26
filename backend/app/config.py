from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PREDFIT_", env_file=".env", extra="ignore")

    app_name: str = "PredFit API"
    environment: str = "dev"

    # SECURITY: override in production
    jwt_secret: str = "dev-secret-change-me"
    jwt_issuer: str = "predfit"
    jwt_access_token_minutes: int = 60 * 24 * 7

    database_url: str = "sqlite:///./predfit.db"
    cors_origins_csv: str = "http://localhost:5173"

    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins_csv.split(",") if o.strip()]


settings = Settings()

