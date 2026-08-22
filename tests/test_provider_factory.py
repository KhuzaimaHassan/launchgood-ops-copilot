"""Unit tests for LLM provider factory configuration and error boundaries."""

import pytest

from app.api.app import create_app
from app.config import AppConfig
from app.providers import get_llm_provider
from app.providers.fake import FakeLLMProvider


def test_factory_returns_fake_llm_provider_for_mock_modes() -> None:
    for mode in ["mock", "fake", "deterministic"]:
        config = AppConfig(llm_provider=mode)
        provider = get_llm_provider(config)
        assert isinstance(provider, FakeLLMProvider)


def test_factory_raises_value_error_for_unsupported_provider() -> None:
    config = AppConfig(llm_provider="unsupported-provider-xyz")
    with pytest.raises(ValueError, match="Unsupported LLM_PROVIDER"):
        get_llm_provider(config)


def test_factory_raises_value_error_for_live_provider_without_api_key() -> None:
    for provider_name in ["openai", "anthropic", "gemini"]:
        config = AppConfig(llm_provider=provider_name, llm_api_key=None)
        with pytest.raises(ValueError, match="LLM_API_KEY is missing"):
            get_llm_provider(config)


def test_factory_raises_not_implemented_error_for_live_provider_with_api_key() -> None:
    for provider_name in ["openai", "anthropic", "gemini"]:
        config = AppConfig(llm_provider=provider_name, llm_api_key="sk-test-key-123")
        with pytest.raises(NotImplementedError, match="requires live adapter package"):
            get_llm_provider(config)


def test_fastapi_app_creation_uses_shared_provider_factory() -> None:
    # Valid mock config succeeds
    valid_config = AppConfig(llm_provider="mock", database_url="sqlite:///:memory:")
    app = create_app(valid_config)
    assert app.title == "LaunchGood Ops Copilot"

    # Invalid provider config raises ValueError on app creation
    invalid_config = AppConfig(llm_provider="invalid-provider", database_url="sqlite:///:memory:")
    with pytest.raises(ValueError, match="Unsupported LLM_PROVIDER"):
        create_app(invalid_config)
