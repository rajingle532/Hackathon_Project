"""
Agentic Service — Configuration
================================
Loads environment variables via pydantic-settings.
All config is centralized here. Other modules import from this file.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── Service ──────────────────────────────────────────────────────
    PORT: int = 8080
    LOG_LEVEL: str = "INFO"
    SERVICE_NAME: str = "krishi-sakhi-agentic"
    SERVICE_VERSION: str = "0.1.0"

    # ── Google Gemini ────────────────────────────────────────────────
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # ── Express Backend ──────────────────────────────────────────────
    BACKEND_BASE_URL: str = "http://localhost:5000"

    # ── Existing ML Services ─────────────────────────────────────────
    ML_API_URL: str = "http://localhost:8001"
    DISEASE_API_URL: str = "http://localhost:5050"

    # ── MongoDB (future: Module 10) ──────────────────────────────────
    MONGO_URI: Optional[str] = None

    # ── ChromaDB (Module 5) ──────────────────────────────────────────
    CHROMA_DB_DIR: str = "./data/chroma"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    KNOWLEDGE_BASE_DIR: str = "./rag/knowledge_base"
    TOP_K_RESULTS: int = 3

    # ── External APIs (Module 4) ─────────────────────────────────────
    WEATHER_API_KEY: str = ""
    WEATHER_API_PROVIDER: str = "openweathermap"
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    DEFAULT_LOCATION: str = "Delhi"
    REQUEST_TIMEOUT_SECONDS: int = 10

    # ── Disease API (Module 6) ───────────────────────────────────────
    DISEASE_API_URL: str = "http://localhost:5050/predict"
    DISEASE_CONFIDENCE_THRESHOLD: float = 0.75
    ENABLE_DISEASE_IMAGE_SUPPORT: bool = True

    # ── Recommendation API (Module 7) ────────────────────────────────
    RECOMMENDATION_API_URL: str = "http://localhost:8001/predict"
    RECOMMENDATION_CONFIDENCE_THRESHOLD: float = 0.70
    DEFAULT_SOIL_TYPE: str = "loamy"
    DEFAULT_SEASON: str = "kharif"
    ENABLE_RECOMMENDATION_FALLBACK: bool = True

    # ── Market API (Module 8) ────────────────────────────────────────
    MARKET_API_URL: str = "http://localhost:5000/api/market/prices"
    DEFAULT_MARKET_LOCATION: str = "Delhi"
    DEFAULT_MARKET_CROP: str = "Wheat"
    MARKET_CONFIDENCE_THRESHOLD: float = 0.70
    ENABLE_MARKET_FALLBACK: bool = True

    # ── Escalation API (Module 9) ────────────────────────────────────
    ENABLE_ESCALATION_AGENT: bool = True
    ESCALATION_CONFIDENCE_THRESHOLD: float = 0.65
    DEFAULT_CONSULTANT_TYPE: str = "Agriculture Officer"
    DEFAULT_ESCALATION_TARGET: str = "Local Agriculture Department"

    # ── Memory & Persistence (Module 10) ─────────────────────────────
    ENABLE_MEMORY: bool = True
    MAX_CHAT_HISTORY_MESSAGES: int = 10
    MAX_PROFILE_CROPS: int = 5
    ENABLE_PROFILE_ENRICHMENT: bool = True
    ENABLE_HISTORY_CONTEXT: bool = True

    # ── MongoDB (Module 11) ──────────────────────────────────────────
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DATABASE: str = "krishi_sakhi"
    FARMER_PROFILE_COLLECTION: str = "farmer_profiles"
    CONVERSATION_COLLECTION: str = "conversation_messages"
    AGENT_INTERACTION_COLLECTION: str = "agent_interactions"
    ENABLE_MONGO_MEMORY: bool = True
    MONGO_TIMEOUT_MS: int = 5000

    # ── Telemetry & Hindsight (Module 12) ────────────────────────────
    FEEDBACK_COLLECTION: str = "feedback_events"
    HINDSIGHT_COLLECTION: str = "hindsight_logs"
    TELEMETRY_COLLECTION: str = "telemetry_events"
    ENABLE_TELEMETRY: bool = True
    ENABLE_HINDSIGHT_LOGGING: bool = True
    DEFAULT_RESPONSE_SCORE: float = 0.5
    LOW_CONFIDENCE_SCORE_THRESHOLD: float = 0.6

    # ── External Hindsight Memory ────────────────────────────────────
    ENABLE_EXTERNAL_HINDSIGHT: bool = True
    HINDSIGHT_PROVIDER: str = "custom"
    HINDSIGHT_API_BASE_URL: str = ""
    HINDSIGHT_API_KEY: str = ""
    HINDSIGHT_PROJECT_ID: str = ""
    HINDSIGHT_TIMEOUT_SECONDS: int = 10
    HINDSIGHT_MAX_RETRIES: int = 3
    HINDSIGHT_USE_SDK: bool = False

    # ── Background Tasks & Async Events (Module 13) ──────────────────
    ENABLE_BACKGROUND_TASKS: bool = True
    ENABLE_ASYNC_PERSISTENCE: bool = True
    ENABLE_ASYNC_TELEMETRY: bool = True
    ENABLE_ASYNC_FEEDBACK: bool = True
    ENABLE_EVENT_NOTIFICATIONS: bool = True
    BACKGROUND_TASK_TIMEOUT_SECONDS: int = 15
    MAX_BACKGROUND_RETRIES: int = 3

    # ── Evaluation Framework & Analytics (Module 14) ─────────────────
    ENABLE_EVALUATION_FRAMEWORK: bool = True
    EVALUATION_REPORTS_DIR: str = "./evaluation/reports"
    GOLDEN_DATASET_DIR: str = "./evaluation/datasets"
    MIN_ACCEPTABLE_RESPONSE_SCORE: float = 0.65
    MIN_ACCEPTABLE_RAG_SCORE: float = 0.60
    ENABLE_AUTOMATED_EVALUATION: bool = False

    # ── Security & Hardening (Module 15) ─────────────────────────────
    ENABLE_AUTH: bool = True
    JWT_SECRET_KEY: str = "replace_me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    ENABLE_API_KEYS: bool = True
    VALID_API_KEYS: str = "dev-key-1,dev-key-2"
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    MAX_REQUEST_SIZE_BYTES: int = 50000
    MAX_MESSAGE_LENGTH: int = 5000
    ENABLE_PII_MASKING: bool = True
    ENABLE_PROMPT_GUARD: bool = True
    ENABLE_INPUT_SANITIZATION: bool = True

    # ── Timeouts ─────────────────────────────────────────────────────
    BACKEND_TIMEOUT: float = 10.0
    ML_TIMEOUT: float = 15.0
    LLM_TIMEOUT: float = 30.0

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def is_llm_configured(self) -> bool:
        return bool(self.GOOGLE_API_KEY and self.GOOGLE_API_KEY != "your_gemini_api_key_here")


# Singleton instance — import this everywhere
settings = Settings()
