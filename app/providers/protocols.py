"""Provider interfaces used by the workflow and deterministic test doubles."""

from dataclasses import dataclass
from typing import Any, Protocol, TypeVar

from app.domain.enums import GroundingStatus

T = TypeVar("T")


@dataclass(frozen=True)
class ProviderMetadata:
    provider: str
    model: str
    request_id: str | None = None


@dataclass(frozen=True)
class PolicyMatch:
    policy_id: str
    chunk_id: str
    excerpt: str
    score: float
    grounding_status: GroundingStatus


class LLMProvider(Protocol):
    def generate_structured(
        self, *, prompt: str, schema: type[T]
    ) -> tuple[T, ProviderMetadata]: ...


class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class PolicyRetriever(Protocol):
    def search(
        self, *, query: str, top_k: int = 5, category: str | None = None
    ) -> tuple[list[PolicyMatch], dict[str, Any]]: ...
