import pytest
from evaluation.golden_dataset_loader import load_dataset, load_all_datasets

def test_load_dataset_missing(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda path: False)
    data = load_dataset("missing.json")
    assert data == []

def test_load_all_datasets(monkeypatch):
    monkeypatch.setattr("os.path.exists", lambda path: True)
    monkeypatch.setattr("os.listdir", lambda path: ["advisory_dataset.json"])
    monkeypatch.setattr("evaluation.golden_dataset_loader.load_dataset", lambda name: [{"input": "test"}])
    
    datasets = load_all_datasets()
    assert "advisory_dataset" in datasets
    assert datasets["advisory_dataset"][0]["input"] == "test"
