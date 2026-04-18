import pytest
from tools.symptom_parser_tool import extract_symptoms, detect_possible_disease
from utils.disease_constants import DEFAULT_DISEASE

def test_extract_symptoms():
    assert "yellow leaves" in extract_symptoms("My plant has yellow leaves and is drying.")
    assert "drying" in extract_symptoms("My plant has yellow leaves and is drying.")
    assert extract_symptoms("Everything is fine") == []

def test_detect_possible_disease():
    assert detect_possible_disease(["yellow leaves"]) == "nutrient_deficiency"
    assert detect_possible_disease(["white powder"]) == "powdery_mildew"
    assert detect_possible_disease([]) == DEFAULT_DISEASE
    assert detect_possible_disease(["unknown_symptom"]) == DEFAULT_DISEASE
