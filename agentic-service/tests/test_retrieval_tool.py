import pytest
from tools.retrieval_tool import retrieve_context

def test_retrieve_context():
    assert "4-6 irrigations" in retrieve_context("wheat irrigation schedule")
    assert "nitrogen deficiency" in retrieve_context("my crop has yellow leaves")
    assert "neem-based" in retrieve_context("how to control pest")
    assert retrieve_context("random unrelated stuff") == ""
