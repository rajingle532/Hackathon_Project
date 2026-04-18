import pytest
from services.retrieval_service import get_retrieval_category, get_retrieval_context

def test_get_retrieval_category():
    assert get_retrieval_category("my leaves are yellow") == "yellow_leaves"
    assert get_retrieval_category("need some urea") == "fertilizer"
    assert get_retrieval_category("random text") == "default"

def test_get_retrieval_context():
    assert "nitrogen deficiency" in get_retrieval_context("my leaves are yellow")
    assert get_retrieval_context("random unrelated text") == ""
