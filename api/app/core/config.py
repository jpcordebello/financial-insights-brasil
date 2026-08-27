from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Configuracoes(BaseSettings):
    db_host: str
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str
    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173")


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def lista_cors_origins(
        self,
    ) -> list[str]:
        return [
            origem.strip()
            for origem in self.cors_origins.split(",")
            if origem.strip()
        ]
@lru_cache
def obter_configuracoes() -> Configuracoes:
    return Configuracoes()