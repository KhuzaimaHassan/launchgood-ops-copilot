"""Dependency-light parser and heading-aware chunker for synthetic policies."""

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PolicyDocument:
    policy_id: str
    title: str
    version: str
    effective_date: str
    category: str
    synthetic: bool
    source_path: str
    content: str


@dataclass(frozen=True)
class PolicyChunk:
    chunk_id: str
    policy_id: str
    title: str
    section_heading: str
    text: str
    ordinal: int
    category: str
    version: str


def _parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    if not raw.startswith("---\n"):
        raise ValueError("policy must begin with YAML-like frontmatter")
    marker = raw.find("\n---", 4)
    if marker < 0:
        raise ValueError("policy frontmatter is not closed")
    metadata: dict[str, str] = {}
    for line in raw[4:marker].splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        metadata[key.strip()] = value
    return metadata, raw[marker + 4 :].strip()


def parse_policy(path: Path) -> PolicyDocument:
    metadata, content = _parse_frontmatter(path.read_text(encoding="utf-8"))
    required = ("policy_id", "title", "version", "effective_date", "category", "synthetic")
    missing = [key for key in required if key not in metadata]
    if missing:
        raise ValueError(f"policy {path} missing metadata: {', '.join(missing)}")
    if metadata["synthetic"].lower() != "true":
        raise ValueError(f"prototype policy must declare synthetic: true: {path}")
    return PolicyDocument(
        policy_id=metadata["policy_id"],
        title=metadata["title"],
        version=metadata["version"],
        effective_date=metadata["effective_date"],
        category=metadata["category"],
        synthetic=True,
        source_path=str(path),
        content=content,
    )


def chunk_policy(document: PolicyDocument, max_words: int = 300) -> list[PolicyChunk]:
    if max_words < 1:
        raise ValueError("max_words must be positive")
    sections = re.split(r"(?=^#{1,6}\s+.+$)", document.content, flags=re.MULTILINE)
    chunks: list[PolicyChunk] = []
    ordinal = 0
    for section in sections:
        section = section.strip()
        if not section:
            continue
        lines = section.splitlines()
        heading = lines[0].lstrip("#").strip() if lines[0].startswith("#") else document.title
        words = " ".join(lines[1:] if lines[0].startswith("#") else lines).split()
        for start in range(0, len(words), max_words):
            text = " ".join(words[start : start + max_words]).strip()
            if not text:
                continue
            ordinal += 1
            chunks.append(
                PolicyChunk(
                    chunk_id=f"{document.policy_id}-{ordinal:03d}",
                    policy_id=document.policy_id,
                    title=document.title,
                    section_heading=heading,
                    text=text,
                    ordinal=ordinal,
                    category=document.category,
                    version=document.version,
                )
            )
    return chunks


def load_policy_documents(directory: Path) -> list[PolicyDocument]:
    return [parse_policy(path) for path in sorted(directory.glob("*.md"))]
