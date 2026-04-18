import json
import os
import logging
from config import settings

log = logging.getLogger("golden_dataset_loader")

def load_dataset(dataset_name: str) -> list[dict]:
    try:
        path = os.path.join(settings.GOLDEN_DATASET_DIR, dataset_name)
        if not os.path.exists(path):
            log.warning(f"Dataset {dataset_name} not found at {path}")
            return []
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        log.error(f"Failed to load dataset {dataset_name}: {e}")
        return []

def load_all_datasets() -> dict:
    datasets = {}
    if not os.path.exists(settings.GOLDEN_DATASET_DIR):
        return datasets
        
    for file in os.listdir(settings.GOLDEN_DATASET_DIR):
        if file.endswith(".json"):
            name = file.split(".")[0]
            datasets[name] = load_dataset(file)
            
    return datasets
