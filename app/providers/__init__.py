"""Provider contracts for LLM, embeddings, and policy retrieval."""

from app.providers.factory import get_llm_provider
from app.providers.fake import FakeLLMProvider
from app.providers.protocols import (
    EmbeddingProvider,
    LLMProvider,
    PolicyMatch,
    PolicyRetriever,
    ProviderMetadata,
)

__all__ = [
    "EmbeddingProvider",
    "FakeLLMProvider",
    "LLMProvider",
    "PolicyMatch",
    "PolicyRetriever",
    "ProviderMetadata",
    "get_llm_provider",
]
