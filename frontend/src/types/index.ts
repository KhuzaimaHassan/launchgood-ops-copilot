export type CaseStatus =
  | "PENDING_ANALYSIS"
  | "AWAITING_HUMAN_DECISION"
  | "RESOLVED"
  | "ESCALATED"
  | "ANALYZING"
  | "NEEDS_REVIEW"
  | "FAILED";

export type RiskLevel = "LOW" | "MEDIUM" | "HIGH";
export type Priority = "LOW" | "MEDIUM" | "HIGH" | "URGENT";
export type ConfidenceTier = "LOW" | "MEDIUM" | "HIGH";
export type DecisionType = "APPROVE" | "MODIFY" | "REJECT" | "ESCALATE";
export type GroundingStatus = "STRONG" | "WEAK" | "NONE";
export type RecommendationAction =
  | "REQUEST_DOCUMENTATION"
  | "INVESTIGATE"
  | "NO_ACTION"
  | "ESCALATE";

export interface Campaign {
  campaign_id: string;
  title: string;
  description: string;
  organizer_summary?: string | null;
  created_at: string;
  updated_at: string;
}

export interface SupportMessage {
  source_id: string;
  case_id: string;
  channel: string;
  author_role: string;
  content: string;
  created_at: string;
}

export interface CampaignUpdate {
  source_id: string;
  campaign_id: string;
  content: string;
  created_at: string;
}

export interface RiskSignal {
  signal_id: string;
  case_id: string;
  signal_type: string;
  value: Record<string, unknown> | string;
  severity: RiskLevel;
  source_ref?: string | null;
  created_at?: string;
}

export interface Case {
  case_id: string;
  campaign: Campaign;
  title: string;
  intake_category: string;
  initial_priority: Priority;
  status: CaseStatus;
  support_messages: SupportMessage[];
  campaign_updates: CampaignUpdate[];
  risk_signals: RiskSignal[];
  created_at: string;
  updated_at: string;
}

export interface PolicyReference {
  policy_reference_id?: string;
  policy_id: string;
  chunk_id: string;
  retrieval_score: number;
  grounding_status: GroundingStatus;
  excerpt: string;
}

export interface EvidenceItem {
  evidence_id?: string;
  source_type: string;
  source_id: string;
  fact: string;
  supports: string;
}

export interface AIAssessment {
  assessment_id?: string;
  analysis_run_id?: string;
  case_id?: string;
  summary?: string;
  category: string;
  risk_level: RiskLevel;
  priority: Priority;
  confidence_score: number;
  confidence_tier: ConfidenceTier;
  evidence: EvidenceItem[];
  policy_references: PolicyReference[];
  recommendation_action: RecommendationAction;
  recommendation_rationale: string;
  uncertainty_flags: string[];
  human_review_required?: boolean;
  escalation_recommended: boolean;
  created_at: string;
}

export interface ReviewerDecision {
  decision_id?: string;
  case_id: string;
  assessment_id?: string | null;
  decision_type: DecisionType;
  overridden_risk?: RiskLevel | null;
  overridden_priority?: Priority | null;
  overridden_recommendation?: string | null;
  reviewer_notes?: string | null;
  reviewer_id: string;
  created_at?: string;
}

export interface AuditEvent {
  event_id: string;
  case_id: string;
  event_type: string;
  actor_type: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export interface EvaluationFailure {
  case_id: string;
  title?: string;
  error?: string;
  mismatches?: Record<string, string>;
  tags?: string[];
}

export interface EvaluationRun {
  run_id: string;
  total: number;
  succeeded: number;
  failed: number;
  failures: EvaluationFailure[];
  metrics: Record<string, number>;
}
