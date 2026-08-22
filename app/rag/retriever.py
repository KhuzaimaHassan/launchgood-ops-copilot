"""PolicyRetriever implementation with configurable grounding thresholds."""

from pathlib import Path
from time import perf_counter

from app.domain.enums import GroundingStatus
from app.providers.protocols import PolicyMatch

from .index import LocalPolicyIndex
from .parser import chunk_policy, load_policy_documents


class LocalPolicyRetriever:
    def __init__(
        self,
        index: LocalPolicyIndex,
        *,
        strong_threshold: float = 0.35,
        weak_threshold: float = 0.15,
        index_version: str = "unversioned",
    ) -> None:
        if weak_threshold >= strong_threshold:
            raise ValueError("weak threshold must be below strong threshold")
        self.index = index
        self.strong_threshold = strong_threshold
        self.weak_threshold = weak_threshold
        self.index_version = index_version

    @classmethod
    def from_policy_directory(
        cls, directory: Path, *, index_version: str = "local-v1"
    ) -> "LocalPolicyRetriever":
        documents = load_policy_documents(directory)
        chunks = [chunk for document in documents for chunk in chunk_policy(document)]
        index = LocalPolicyIndex()
        index.build(chunks)
        return cls(index, index_version=index_version)

    def search(
        self, *, query: str, top_k: int = 5, category: str | None = None
    ) -> tuple[list[PolicyMatch], dict[str, object]]:
        started = perf_counter()
        ranked = self.index.search(query, top_k=top_k, category=category)
        matches: list[PolicyMatch] = []
        for chunk, score in ranked:
            if score < self.weak_threshold:
                continue
            grounding = (
                GroundingStatus.STRONG if score >= self.strong_threshold else GroundingStatus.WEAK
            )
            matches.append(
                PolicyMatch(
                    policy_id=chunk.policy_id,
                    chunk_id=chunk.chunk_id,
                    excerpt=chunk.text,
                    score=score,
                    grounding_status=grounding,
                )
            )
        metadata = {
            "query": query,
            "top_k": top_k,
            "category": category,
            "index_version": self.index_version,
            "grounding_status": (
                matches[0].grounding_status.value if matches else GroundingStatus.NONE.value
            ),
            "duration_ms": round((perf_counter() - started) * 1000, 3),
        }
        return matches, metadata
