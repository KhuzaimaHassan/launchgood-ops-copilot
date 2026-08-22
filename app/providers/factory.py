"""LLM Provider Factory respecting application configuration.

The prototype currently supports 'mock' (and aliases 'fake', 'deterministic') as the
active, deterministic provider for offline verification. Reserved live provider options
('openai', 'anthropic', 'gemini') validate configuration (requiring LLM_API_KEY) and
raise NotImplementedError until live SDK adapters are installed.
"""

from app.config import AppConfig
from app.providers.fake import FakeLLMProvider
from app.providers.protocols import LLMProvider


def get_llm_provider(config: AppConfig) -> LLMProvider:
    """Instantiate and return the configured LLM provider.

    Returns:
        LLMProvider: Active LLM provider instance (FakeLLMProvider for mock mode).

    Raises:
        ValueError: If provider name is unknown or missing required API keys.
        NotImplementedError: If a reserved live provider is configured without an adapter.
    """
    provider_name = (config.llm_provider or "mock").lower().strip()

    if provider_name in {"mock", "fake", "deterministic"}:
        return FakeLLMProvider()

    if provider_name in {"openai", "anthropic", "gemini"}:
        if not config.llm_api_key:
            raise ValueError(
                f"LLM_PROVIDER '{config.llm_provider}' is configured but LLM_API_KEY is missing."
            )
        raise NotImplementedError(
            f"Live LLM provider '{config.llm_provider}' requires live adapter package. "
            "Use LLM_PROVIDER=mock for offline prototype verification."
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER '{config.llm_provider}'. "
        "Valid options: 'mock', 'fake', 'deterministic'."
    )
