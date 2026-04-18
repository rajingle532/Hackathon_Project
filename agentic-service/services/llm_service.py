"""
Agentic Service — LLM Service
===============================
Wrapper around Google Gemini with error handling and fallback.
This is the single point of LLM access for the entire agentic service.
"""

import google.generativeai as genai
from config import settings
from utils.logger import setup_logger

log = setup_logger("llm")

# ── Gemini model fallback chain ──────────────────────────────────────
MODEL_CHAIN = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

_configured = False


def configure_gemini():
    """Configure the Gemini SDK with the API key. Called once at startup."""
    global _configured
    if _configured:
        return

    if not settings.is_llm_configured:
        log.warning("GOOGLE_API_KEY not set — LLM calls will fail")
        return

    genai.configure(api_key=settings.GOOGLE_API_KEY)
    _configured = True
    log.info(f"Gemini configured. Model chain: {', '.join(MODEL_CHAIN)}")


async def call_llm(
    prompt: str,
    system_instruction: str = "",
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """
    Call Gemini with automatic model fallback.

    Args:
        prompt: The user prompt text.
        system_instruction: Optional system-level instruction.
        temperature: Sampling temperature.
        max_tokens: Max output tokens.

    Returns:
        The LLM response text.

    Raises:
        RuntimeError: If all models fail.
    """
    configure_gemini()

    if not settings.is_llm_configured:
        return "[LLM not configured — set GOOGLE_API_KEY in .env]"

    # Determine which model to try first
    preferred = settings.GEMINI_MODEL
    models_to_try = [preferred] + [m for m in MODEL_CHAIN if m != preferred]

    last_error = None

    for model_name in models_to_try:
        try:
            log.info(f"Calling Gemini model: {model_name}")

            model_kwargs = {"model_name": model_name}
            if system_instruction:
                model_kwargs["system_instruction"] = system_instruction

            model = genai.GenerativeModel(**model_kwargs)

            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )

            text = response.text
            if not text:
                raise ValueError("Empty response from Gemini")

            log.info(f"LLM response received ({len(text)} chars) from {model_name}")
            return text

        except Exception as e:
            last_error = e
            error_msg = str(e).lower()
            log.warning(f"Model {model_name} failed: {str(e)[:120]}")

            # Retryable errors — try next model
            retryable = any(
                kw in error_msg
                for kw in ["quota", "429", "resource_exhausted", "rate limit",
                           "not found", "404", "deprecated", "overloaded",
                           "unavailable", "503"]
            )

            if not retryable:
                raise  # Non-retryable error — don't try other models

    raise RuntimeError(f"All Gemini models exhausted. Last error: {last_error}")


async def check_llm_health() -> bool:
    """Quick health check — attempt a minimal LLM call."""
    try:
        result = await call_llm("Reply with exactly: OK", max_tokens=10)
        return bool(result)
    except Exception:
        return False
