def normalize_language(language: str) -> str:
    lang_lower = language.lower().strip()
    mapping = {
        "en": "English",
        "english": "English",
        "hi": "Hindi",
        "hindi": "Hindi",
        "mr": "Marathi",
        "marathi": "Marathi",
        "pa": "Punjabi",
        "punjabi": "Punjabi",
        "gu": "Gujarati",
        "gujarati": "Gujarati"
    }
    return mapping.get(lang_lower, "English")
