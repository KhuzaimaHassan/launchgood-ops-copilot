"""Deterministic fake LLM provider for offline workflow tests."""

import json
from typing import TypeVar

from app.domain.enums import Priority, RecommendationAction, RiskLevel
from app.providers.protocols import ProviderMetadata
from app.workflow.state import AssessmentDraft

T = TypeVar("T")


class FakeLLMProvider:
    def generate_structured(self, *, prompt: str, schema: type[T]) -> tuple[T, ProviderMetadata]:
        marker = "WORKFLOW_CONTEXT_JSON="
        context = json.loads(prompt.split(marker, 1)[1])
        signals = context["normalized_signals"]
        category = signals["issue_category_candidates"][0]
        # Conflicting records need urgent review even without an intake risk signal.
        needs_attention = bool(signals["risk_indicators"] or context["conflicts"])
        risk = RiskLevel.HIGH if needs_attention else RiskLevel.LOW
        priority = Priority.HIGH if needs_attention else Priority.LOW
        action = (
            RecommendationAction.REQUEST_DOCUMENTATION
            if category == "DOCUMENTATION_CONCERN"
            else RecommendationAction.NO_ACTION
        )
        draft = AssessmentDraft(
            summary=f"Synthetic assessment for {category.lower().replace('_', ' ')}.",
            category=category,
            risk_level=risk.value,
            priority=priority.value,
            confidence_score=0.84 if risk is RiskLevel.HIGH else 0.88,
            evidence=context["evidence_items"],
            recommendation_action=action.value,
            recommendation_rationale="Recommendation is based on the available synthetic source evidence.",
            human_review_required=True,
            escalation_recommended=bool(context["conflicts"]),
        )
        return draft, ProviderMetadata(provider="fake", model="deterministic-v1")
