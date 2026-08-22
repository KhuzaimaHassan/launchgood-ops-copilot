"""Environment-backed configuration for the application boundary."""

import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    app_env: str = "development"
    database_url: str = f"sqlite:///{PROJECT_ROOT / 'data' / 'app.db'}"
    llm_provider: str = "mock"
    llm_model: str = "mock-model"
    llm_api_key: str | None = None
    embedding_provider: str = "local"
    embedding_model: str = "sentence-transformers"
    rag_index_path: str = str(PROJECT_ROOT / "data" / "index" / "policies.faiss")
    rag_index_version: str = "unbuilt"
    confidence_high_threshold: float = Field(default=0.80, ge=0.0, le=1.0)
    confidence_medium_threshold: float = Field(default=0.55, ge=0.0, le=1.0)
    max_analysis_retries: int = Field(default=1, ge=0, le=3)
    request_timeout_seconds: float = Field(default=30.0, gt=0.0)

    @field_validator("confidence_medium_threshold")
    @classmethod
    def medium_threshold_below_high(cls, value: float, info):
        high = info.data.get("confidence_high_threshold", 0.80)
        if value >= high:
            raise ValueError("medium confidence threshold must be below high threshold")
        return value

    @classmethod
    def from_env(cls) -> "AppConfig":
        values: dict[str, object] = {}
        mapping = {
            "APP_ENV": "app_env",
            "DATABASE_URL": "database_url",
            "LLM_PROVIDER": "llm_provider",
            "LLM_MODEL": "llm_model",
            "LLM_API_KEY": "llm_api_key",
            "EMBEDDING_PROVIDER": "embedding_provider",
            "EMBEDDING_MODEL": "embedding_model",
            "RAG_INDEX_PATH": "rag_index_path",
            "RAG_INDEX_VERSION": "rag_index_version",
        }
        for env_name, field_name in mapping.items():
            if (value := os.getenv(env_name)) is not None:
                values[field_name] = value
        for env_name, field_name, converter in (
            ("CONFIDENCE_HIGH_THRESHOLD", "confidence_high_threshold", float),
            ("CONFIDENCE_MEDIUM_THRESHOLD", "confidence_medium_threshold", float),
            ("MAX_ANALYSIS_RETRIES", "max_analysis_retries", int),
            ("REQUEST_TIMEOUT_SECONDS", "request_timeout_seconds", float),
        ):
            if (value := os.getenv(env_name)) is not None:
                values[field_name] = converter(value)
        return cls(**values)
