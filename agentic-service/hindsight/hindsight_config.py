from config import settings

class HindsightConfig:
    @property
    def enabled(self) -> bool:
        return settings.ENABLE_EXTERNAL_HINDSIGHT

    @property
    def base_url(self) -> str:
        return settings.HINDSIGHT_API_BASE_URL

    @property
    def api_key(self) -> str:
        return settings.HINDSIGHT_API_KEY

    @property
    def project_id(self) -> str:
        return settings.HINDSIGHT_PROJECT_ID

    @property
    def timeout(self) -> int:
        return settings.HINDSIGHT_TIMEOUT_SECONDS

    @property
    def max_retries(self) -> int:
        return settings.HINDSIGHT_MAX_RETRIES

hindsight_config = HindsightConfig()
