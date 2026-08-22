"""Stable domain enum values shared by API, persistence, and UI contracts."""

from enum import StrEnum


class CaseStatus(StrEnum):
    PENDING_ANALYSIS = "PENDING_ANALYSIS"
    AWAITING_HUMAN_DECISION = "AWAITING_HUMAN_DECISION"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"
    ANALYZING = "ANALYZING"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    FAILED = "FAILED"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Priority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class ConfidenceTier(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DecisionType(StrEnum):
    APPROVE = "APPROVE"
    MODIFY = "MODIFY"
    REJECT = "REJECT"
    ESCALATE = "ESCALATE"


class GroundingStatus(StrEnum):
    STRONG = "STRONG"
    WEAK = "WEAK"
    NONE = "NONE"


class RecommendationAction(StrEnum):
    REQUEST_DOCUMENTATION = "REQUEST_DOCUMENTATION"
    INVESTIGATE = "INVESTIGATE"
    NO_ACTION = "NO_ACTION"
    ESCALATE = "ESCALATE"


class SourceType(StrEnum):
    CAMPAIGN = "CAMPAIGN"
    MESSAGE = "MESSAGE"
    UPDATE = "UPDATE"
    RISK_SIGNAL = "RISK_SIGNAL"
