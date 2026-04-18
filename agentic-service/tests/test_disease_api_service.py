import pytest
from services.disease_api_service import predict_crop_disease
from utils.disease_constants import DEFAULT_DISEASE
from utils.disease_fallbacks import DISEASE_API_FALLBACK

def test_predict_crop_disease_no_image_with_symptoms():
    result = predict_crop_disease(image_path=None, symptoms=["yellow leaves"])
    assert result["success"] == True
    assert result["disease_name"] == "Nutrient Deficiency"
    assert result["confidence"] == 0.50

def test_predict_crop_disease_no_image_no_symptoms():
    result = predict_crop_disease(image_path=None, symptoms=[])
    assert result["success"] == False
    assert result["disease_name"] == DEFAULT_DISEASE
    assert result["treatment"] == DISEASE_API_FALLBACK

def test_predict_crop_disease_mock_api(monkeypatch):
    import config
    monkeypatch.setattr(config.settings, "ENABLE_DISEASE_IMAGE_SUPPORT", True)
    # The actual implementation currently mocks the response anyway, so we just call it
    result = predict_crop_disease(image_path="dummy.jpg")
    assert result["success"] == True
    assert result["disease_name"] == "Mock Disease API Output"
