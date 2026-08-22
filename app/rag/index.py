"""Persisted local vector index with a dependency-free cosine-search backend."""

import json
from dataclasses import asdict
from pathlib import Path

from .embeddings import HashEmbeddingProvider
from .parser import PolicyChunk


class LocalPolicyIndex:
    def __init__(self, embedder: HashEmbeddingProvider | None = None) -> None:
        self.embedder = embedder or HashEmbeddingProvider()
        self.chunks: list[PolicyChunk] = []
        self.vectors: list[list[float]] = []

    def build(self, chunks: list[PolicyChunk]) -> None:
        self.chunks = list(chunks)
        self.vectors = self.embedder.embed([chunk.text for chunk in self.chunks])

    def search(self, query: str, top_k: int = 5, category: str | None = None) -> list[tuple[PolicyChunk, float]]:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        query_vector = self.embedder.embed([query])[0]
        candidates = [
            (chunk, vector)
            for chunk, vector in zip(self.chunks, self.vectors)
            if category is None or chunk.category == category
        ]
        ranked = sorted(
            ((chunk, sum(left * right for left, right in zip(query_vector, vector))) for chunk, vector in candidates),
            key=lambda item: item[1],
            reverse=True,
        )
        return ranked[:top_k]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "dimension": self.embedder.dimension,
            "chunks": [asdict(chunk) for chunk in self.chunks],
            "vectors": self.vectors,
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "LocalPolicyIndex":
        payload = json.loads(path.read_text(encoding="utf-8"))
        index = cls(HashEmbeddingProvider(dimension=payload["dimension"]))
        index.chunks = [PolicyChunk(**chunk) for chunk in payload["chunks"]]
        index.vectors = payload["vectors"]
        return index


class FaissPolicyIndex:
    """Optional FAISS-backed index for deployment environments with faiss-cpu."""

    def __init__(self, embedder: HashEmbeddingProvider | None = None) -> None:
        try:
            import faiss  # type: ignore[import-not-found]
            import numpy as np  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError("FaissPolicyIndex requires the optional 'rag' dependencies") from exc
        self.faiss = faiss
        self.np = np
        self.embedder = embedder or HashEmbeddingProvider()
        self.chunks: list[PolicyChunk] = []
        self.index = faiss.IndexFlatIP(self.embedder.dimension)

    def build(self, chunks: list[PolicyChunk]) -> None:
        self.chunks = list(chunks)
        vectors = self.np.asarray(self.embedder.embed([chunk.text for chunk in chunks]), dtype="float32")
        self.index = self.faiss.IndexFlatIP(self.embedder.dimension)
        if len(vectors):
            self.index.add(vectors)

    def search(self, query: str, top_k: int = 5, category: str | None = None):
        if category is not None:
            candidates = [
                (index, chunk)
                for index, chunk in enumerate(self.chunks)
                if chunk.category == category
            ]
            if not candidates:
                return []
            filtered = self.np.asarray(
                self.embedder.embed([chunk.text for _, chunk in candidates]), dtype="float32"
            )
            query_vector = self.np.asarray(self.embedder.embed([query]), dtype="float32")
            scores = filtered @ query_vector[0]
            ranked = sorted(zip(candidates, scores), key=lambda item: float(item[1]), reverse=True)
            return [(chunk, float(score)) for ((_, chunk), score) in ranked[:top_k]]
        query_vector = self.np.asarray(self.embedder.embed([query]), dtype="float32")
        scores, indices = self.index.search(query_vector, top_k)
        return [
            (self.chunks[index], float(score))
            for score, index in zip(scores[0], indices[0])
            if index >= 0
        ]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.faiss.write_index(self.index, str(path))
        path.with_suffix(path.suffix + ".metadata.json").write_text(
            json.dumps(
                {
                    "dimension": self.embedder.dimension,
                    "chunks": [asdict(chunk) for chunk in self.chunks],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "FaissPolicyIndex":
        index = cls()
        index.index = index.faiss.read_index(str(path))
        metadata = json.loads(path.with_suffix(path.suffix + ".metadata.json").read_text(encoding="utf-8"))
        index.chunks = [PolicyChunk(**chunk) for chunk in metadata["chunks"]]
        return index
