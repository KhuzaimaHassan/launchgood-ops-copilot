from pathlib import Path

from app.domain.enums import GroundingStatus
from app.rag.index import LocalPolicyIndex
from app.rag.parser import chunk_policy, load_policy_documents
from app.rag.retriever import LocalPolicyRetriever

POLICY_DIR = Path("data/policies")


def test_policy_parser_and_chunker_load_synthetic_documents() -> None:
    documents = load_policy_documents(POLICY_DIR)
    chunks = [chunk for document in documents for chunk in chunk_policy(document)]
    assert len(documents) == 2
    assert chunks
    assert all(chunk.policy_id.startswith("POL-") for chunk in chunks)


def test_local_index_round_trips_and_retrieves() -> None:
    documents = load_policy_documents(POLICY_DIR)
    chunks = [chunk for document in documents for chunk in chunk_policy(document)]
    index = LocalPolicyIndex()
    index.build(chunks)
    path = Path(".tmp-policy-index.json")
    try:
        index.save(path)
        loaded = LocalPolicyIndex.load(path)
        results = loaded.search("missing medical campaign documentation")
        assert results
    finally:
        path.unlink(missing_ok=True)


def test_retriever_exposes_grounding_metadata() -> None:
    retriever = LocalPolicyRetriever.from_policy_directory(POLICY_DIR)
    matches, metadata = retriever.search(query="missing documentation for medical campaign")
    assert matches
    assert matches[0].grounding_status in {GroundingStatus.STRONG, GroundingStatus.WEAK}
    assert metadata["index_version"] == "local-v1"
