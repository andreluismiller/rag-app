"""Configuracoes centrais da aplicacao, carregadas a partir do .env."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # OpenAI (necessario apenas nas fases futuras: chat com LLM)
    openai_api_key: str | None = None
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"  # TODO: remover ao migrar para FastEmbed

    # Qdrant (necessario ja na fase 1: ingestao)
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "mec_faq"

    # Postgres (necessario apenas nas fases futuras: metricas/feedback/dashboard)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "raguser"
    postgres_password: str = "ragpassword"
    postgres_db: str = "ragdb"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
