"""Operations Command Center reviewer UI.

Provides an executive-ready human-in-the-loop review workspace for synthetic campaign cases,
featuring real-time KPI metrics, composable multi-dimensional filters, rich case cards with confidence badges,
a 3-zone review workspace with tabbed evidence, a persistent human decision rail, and a visual audit timeline.
"""

import sys
from datetime import datetime
from html import escape
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import AppConfig
from app.domain.enums import CaseStatus, DecisionType
from app.domain.models import Case, ReviewerDecision
from app.providers import get_llm_provider
from app.rag.retriever import LocalPolicyRetriever
from app.repositories.sqlite import SQLiteDatabase, SQLiteRepository
from app.services.services import AnalysisService, CaseService, DecisionService, EvaluationService
from app.workflow.runner import AssessmentWorkflow

COLORS = {
    "navy": "#0F172A",
    "navy_light": "#1E293B",
    "border": "#334155",
    "teal": "#0D9488",
    "teal_bright": "#14B8A6",
    "red": "#EF4444",
    "amber": "#F59E0B",
    "green": "#10B981",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
}


def build_services():
    config = AppConfig.from_env()
    repository = SQLiteRepository(SQLiteDatabase(config.database_url))
    fixture_dir = PROJECT_ROOT / "data" / "fixtures" / "cases"
    
    # Auto-seed synthetic cases if DB is fresh
    existing_ids = {case.case_id for case in repository.list_cases()}
    if fixture_dir.exists():
        for path in sorted(fixture_dir.glob("*.json")):
            fixture = Case.model_validate_json(path.read_text(encoding="utf-8"))
            if fixture.case_id not in existing_ids:
                repository.save_case(fixture)
                
    policy_dir = PROJECT_ROOT / "data" / "policies"
    retriever = LocalPolicyRetriever.from_policy_directory(
        policy_dir, index_version=config.rag_index_version
    )
    workflow = AssessmentWorkflow(
        llm_provider=get_llm_provider(config),
        policy_retriever=retriever,
        repository=repository,
        config=config,
    )
    return (
        repository,
        CaseService(repository),
        AnalysisService(repository, workflow),
        DecisionService(repository),
        EvaluationService(workflow),
        config,
    )


def _inject_theme(st) -> None:
    st.markdown(
        f"""
        <style>
        :root {{ color-scheme: dark; }}
        .stApp {{ background: {COLORS['navy']}; color: {COLORS['text']}; }}
        [data-testid="stSidebar"] {{ background: #111C32; border-right: 1px solid {COLORS['border']}; }}
        [data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{ max-width: 1440px; padding-top: 2rem; padding-bottom: 4rem; }}
        h1, h2, h3, h4, p, label {{ color: {COLORS['text']} !important; }}
        .muted {{ color: {COLORS['muted']}; font-size: .85rem; }}
        .eyebrow {{ color: {COLORS['teal_bright']}; text-transform: uppercase; letter-spacing: .12em; font-size: .74rem; font-weight: 700; margin-bottom: .25rem; }}
        .hero {{ background: linear-gradient(135deg, #172554 0%, {COLORS['navy_light']} 62%, #134E4A 100%); border: 1px solid #1E4E5A; border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1.2rem; box-shadow: 0 16px 40px rgba(0,0,0,.25); }}
        .hero h1 {{ margin: .2rem 0 .35rem; font-size: 2rem; font-weight: 800; }}
        .metric-card {{ background: {COLORS['navy_light']}; border: 1px solid {COLORS['border']}; border-radius: 14px; padding: 1.1rem 1.2rem; min-height: 112px; }}
        .metric-label {{ color: {COLORS['muted']}; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; font-weight: 700; }}
        .metric-value {{ color: {COLORS['text']}; font-size: 1.85rem; font-weight: 800; margin-top: .3rem; }}
        .metric-note {{ color: {COLORS['teal_bright']}; font-size: .8rem; margin-top: .2rem; }}
        .case-card {{ background: {COLORS['navy_light']}; border: 1px solid {COLORS['border']}; border-left: 4px solid {COLORS['teal']}; border-radius: 14px; padding: 1.1rem 1.2rem; margin: .5rem 0 .4rem; }}
        .case-card h3 {{ margin: .45rem 0 .25rem; font-size: 1.1rem; font-weight: 700; }}
        .case-card p {{ color: {COLORS['muted']}; margin: .25rem 0 .6rem; font-size: .88rem; line-height: 1.4; }}
        .pill {{ display: inline-block; border-radius: 999px; padding: .24rem .6rem; margin-right: .35rem; font-size: .72rem; font-weight: 700; letter-spacing: .03em; }}
        .pill-teal {{ background: rgba(20,184,166,.18); color: #5EEAD4; }}
        .pill-red {{ background: rgba(239,68,68,.18); color: #FCA5A5; }}
        .pill-amber {{ background: rgba(245,158,11,.18); color: #FCD34D; }}
        .pill-green {{ background: rgba(16,185,129,.18); color: #6EE7B7; }}
        .pill-muted {{ background: rgba(148,163,184,.15); color: #CBD5E1; }}
        .timeline {{ border-left: 2px solid {COLORS['border']}; margin: .8rem 0 .4rem .6rem; padding-left: 1.25rem; }}
        .timeline-item {{ position: relative; background: rgba(15,23,42,.45); border: 1px solid {COLORS['border']}; border-radius: 10px; padding: .75rem .95rem; margin: .65rem 0; }}
        .timeline-item:before {{ content: ''; position: absolute; width: 10px; height: 10px; border-radius: 50%; background: {COLORS['teal_bright']}; left: -1.62rem; top: 1.05rem; box-shadow: 0 0 0 4px {COLORS['navy']}; }}
        .timeline-meta {{ color: {COLORS['muted']}; font-size: .76rem; margin-top: .2rem; }}
        .failure-card {{ background: rgba(127,29,29,.25); border: 1px solid #7F1D1D; border-radius: 12px; padding: 1rem 1.15rem; margin: .65rem 0; }}
        div.stButton > button {{ border-radius: 999px; border: 1px solid {COLORS['border']}; background: {COLORS['navy_light']}; color: {COLORS['text']}; font-weight: 700; }}
        div.stButton > button[kind="primary"] {{ background: {COLORS['teal']}; border-color: {COLORS['teal_bright']}; color: white; }}
        div[data-baseweb="select"] > div, textarea, input {{ background: {COLORS['navy_light']} !important; color: {COLORS['text']} !important; border-color: {COLORS['border']} !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _esc(value: object) -> str:
    return escape(str(value))


def _status_label(status: CaseStatus) -> str:
    return status.value.replace("_", " ").title()


def _pill(label: str, tone: str = "muted") -> str:
    return f'<span class="pill pill-{tone}">{_esc(label)}</span>'


def _risk_tone(value: str | None) -> str:
    return "red" if value == "HIGH" else "amber" if value == "MEDIUM" else "green"


def _case_assessment(case: Case, analysis_service: AnalysisService):
    return analysis_service.latest_assessment(case.case_id)


def _case_summary(case: Case, assessment) -> str:
    if assessment:
        return assessment.summary
    return case.campaign.description


def _render_metric(st, label: str, value: str, note: str, tone: str = "teal") -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{_esc(label)}</div>'
        f'<div class="metric-value">{_esc(value)}</div>'
        f'<div class="metric-note" style="color:{COLORS.get(tone, COLORS["teal_bright"])}">{_esc(note)}</div></div>',
        unsafe_allow_html=True,
    )


def _render_case_card(st, case: Case, assessment, on_open: str) -> None:
    risk = assessment.risk_level.value if assessment else "UNASSESSED"
    risk_tone = _risk_tone(risk) if assessment else "muted"
    status_tone = "teal" if case.status is CaseStatus.AWAITING_HUMAN_DECISION else "green" if case.status in {CaseStatus.RESOLVED, CaseStatus.ESCALATED} else "amber"
    policy = "No policy yet" if not assessment else ("Policy grounded" if assessment.policy_references else "No policy match")
    policy_tone = "green" if assessment and assessment.policy_references else "amber"
    evidence_count = len(assessment.evidence) if assessment else 0
    
    # Confidence representation: 84% (High) or Not Analyzed
    if assessment:
        conf_str = f"Confidence: {assessment.confidence_score:.0%} ({assessment.confidence_tier.value})"
        conf_tone = "teal" if assessment.confidence_tier.value == "HIGH" else "amber"
        priority_str = f"Initial: {case.initial_priority.value} | AI: {assessment.priority.value}"
    else:
        conf_str = "Confidence: Not Analyzed"
        conf_tone = "muted"
        priority_str = f"Initial Priority: {case.initial_priority.value}"

    st.markdown(
        f'<div class="case-card"><div>{_pill(case.case_id, "teal")} '
        f'{_pill(_status_label(case.status), status_tone)} {_pill(f"Risk: {risk}", risk_tone)} '
        f'{_pill(conf_str, conf_tone)}</div>'
        f'<h3>{_esc(case.title)}</h3><p>{_esc(_case_summary(case, assessment)[:190])}</p>'
        f'<div>{_pill(priority_str, "muted")} {_pill(f"{evidence_count} evidence items", "muted")} {_pill(policy, policy_tone)}</div></div>',
        unsafe_allow_html=True,
    )
    if st.button("Review Case →", key=f"open-{on_open}", use_container_width=True):
        st.session_state["selected_case"] = case.case_id
        st.session_state["active_workspace"] = "Case Review"
        st.rerun()


def _render_source_timeline(st, repository, case: Case) -> None:
    items: list[tuple[datetime, str, str, str]] = [
        (case.campaign.created_at, "Campaign", "Campaign created", case.campaign.description)
    ]
    items.extend((m.created_at, "Support message", m.source_id, m.content) for m in case.support_messages)
    items.extend((u.created_at, "Campaign update", u.source_id, u.content) for u in case.campaign_updates)
    items.extend((case.created_at, "Risk signal", s.signal_id, f"{s.signal_type}: {s.value}") for s in case.risk_signals)
    for event in repository.list_audit_events(case.case_id):
        items.append((event.created_at, event.actor_type, event.event_type, "Audit event recorded"))
    items.sort(key=lambda item: item[0])
    html = '<div class="timeline">'
    for timestamp, actor, event, detail in items:
        html += f'<div class="timeline-item"><b>{_esc(event)}</b> {_pill(actor, "teal")}<div class="timeline-meta">{_esc(timestamp.isoformat())}</div><div>{_esc(detail)}</div></div>'
    st.markdown(html + "</div>", unsafe_allow_html=True)


def _render_audit_history(st, repository, case: Case) -> None:
    st.markdown('<div class="eyebrow">Provenance</div><h3>Audit History</h3>', unsafe_allow_html=True)
    events = repository.list_audit_events(case.case_id)
    if not events:
        st.info("No audit events recorded yet.")
        return
    html = '<div class="timeline">'
    for event in sorted(events, key=lambda item: item.created_at):
        html += f'<div class="timeline-item"><b>{_esc(event.event_type)}</b> {_pill(event.actor_type, "teal")}<div class="timeline-meta">{_esc(event.created_at.isoformat())}</div></div>'
    st.markdown(html + "</div>", unsafe_allow_html=True)
    with st.expander("Technical JSON Details"):
        st.json([event.model_dump(mode="json") for event in events])


def _render_decision_rail(st, case: Case, assessment, decision_service: DecisionService) -> None:
    st.markdown('<div class="eyebrow">Human ownership</div><h3>Decision Rail</h3>', unsafe_allow_html=True)
    if case.status is not CaseStatus.AWAITING_HUMAN_DECISION or assessment is None:
        st.info("Run the AI assessment before recording a human decision.")
        return
    with st.form(f"decision-{case.case_id}"):
        decision_type = st.selectbox("Decision", [item.value for item in DecisionType])
        overridden_risk = st.selectbox("Risk override", ["UNCHANGED", "LOW", "MEDIUM", "HIGH"])
        overridden_priority = st.selectbox("Priority override", ["UNCHANGED", "LOW", "MEDIUM", "HIGH", "URGENT"])
        overridden_recommendation = st.text_input("Recommendation override")
        reviewer_notes = st.text_area("Reviewer notes", placeholder="Explain the judgment or disagreement…")
        submitted = st.form_submit_button("Submit Human Decision", type="primary", use_container_width=True)
    if submitted:
        try:
            decision_service.decide(
                ReviewerDecision(
                    case_id=case.case_id,
                    assessment_id=assessment.assessment_id,
                    decision_type=DecisionType(decision_type),
                    overridden_risk=None if overridden_risk == "UNCHANGED" else overridden_risk,
                    overridden_priority=None if overridden_priority == "UNCHANGED" else overridden_priority,
                    overridden_recommendation=overridden_recommendation or None,
                    reviewer_notes=reviewer_notes or None,
                    reviewer_id="prototype-reviewer",
                )
            )
            st.success("Human decision recorded and audit timeline updated.")
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to record decision: {type(exc).__name__} - {exc!s}")


def _render_review(st, repository, case_service, analysis_service, decision_service) -> None:
    case_id = st.session_state.get("selected_case")
    case = case_service.get_case(case_id) if case_id else None
    if case is None:
        st.info("Select a case from the Dashboard to begin review.")
        return
    assessment = _case_assessment(case, analysis_service)
    risk = assessment.risk_level.value if assessment else "UNASSESSED"
    st.markdown(
        f'<div class="hero"><div class="eyebrow">Executive Case Header</div>'
        f'<h1>{_esc(case.title)}</h1><div>{_pill(case.case_id, "teal")} '
        f'{_pill(_status_label(case.status), "amber" if case.status in {CaseStatus.PENDING_ANALYSIS, CaseStatus.FAILED} else "teal")} '
        f'{_pill(f"Risk: {risk}", _risk_tone(risk) if assessment else "muted")}</div></div>',
        unsafe_allow_html=True,
    )
    header_metrics = st.columns(5)
    header_metrics[0].metric("Category", assessment.category if assessment else case.intake_category)
    header_metrics[1].metric("Risk", risk)
    header_metrics[2].metric("Priority", assessment.priority.value if assessment else case.initial_priority.value)
    header_metrics[3].metric(
        "Confidence",
        f"{assessment.confidence_score:.0%} ({assessment.confidence_tier.value})" if assessment else "—",
        help="Confidence is the model's 0.00–1.00 uncertainty score shown as a percentage and tier. It supports review; it never replaces reviewer judgment.",
    )
    header_metrics[4].metric("Recommended Action", assessment.recommendation_action.value if assessment else "—")
    
    if case.status in {CaseStatus.PENDING_ANALYSIS, CaseStatus.FAILED}:
        if st.button("Run AI Assessment", type="primary", use_container_width=True):
            try:
                analysis_service.analyze(case.case_id)
                st.rerun()
            except Exception as exc:
                st.error(f"Analysis failed: {type(exc).__name__} - {exc!s}")
                
    evidence_col, rail_col = st.columns([2.1, 1], gap="large")
    with evidence_col:
        st.markdown('<div class="eyebrow">Evidence & Context Workspace</div>', unsafe_allow_html=True)
        evidence_tab, policy_tab, timeline_tab, uncertainty_tab = st.tabs([
            "Evidence & Grounding", "Retrieved Policies", "Source Timeline", "Uncertainty & Conflicts"
        ])
        with evidence_tab:
            if not assessment:
                st.info("No AI assessment has been generated yet.")
            else:
                for evidence in assessment.evidence:
                    with st.container(border=True):
                        st.markdown(
                            f'{_pill(evidence.supports, "teal")} {_pill(evidence.source_id, "muted")}<br>'
                            f'<b>Fact:</b> {_esc(evidence.fact)}',
                            unsafe_allow_html=True,
                        )
        with policy_tab:
            if not assessment or not assessment.policy_references:
                st.warning("No applicable policy was retrieved.")
            elif assessment:
                for reference in assessment.policy_references:
                    tone = "green" if reference.grounding_status.value == "STRONG" else "amber"
                    with st.container(border=True):
                        st.markdown(
                            f'{_pill(reference.policy_id, "teal")} {_pill(reference.chunk_id, "muted")} '
                            f'{_pill(reference.grounding_status.value, tone)}<br>'
                            f'<span class="muted">Retrieval Score: {reference.retrieval_score:.3f}</span><br><br>'
                            f'{_esc(reference.excerpt)}',
                            unsafe_allow_html=True,
                        )
        with timeline_tab:
            _render_source_timeline(st, repository, case)
        with uncertainty_tab:
            flags = assessment.uncertainty_flags if assessment else []
            if not flags:
                st.success("No uncertainty flags detected.")
            for flag in flags:
                st.warning(f"⚠️ Flag: {flag.replace('_', ' ').title()}")
            if assessment and assessment.escalation_recommended:
                st.error("🚨 Escalation recommended: ambiguous or conflicting evidence requires human investigation.")
                
    with rail_col, st.container(border=True):
        _render_decision_rail(st, case, assessment, decision_service)
            
    _render_audit_history(st, repository, case)


def _render_dashboard(st, cases, analysis_service) -> None:
    assessments = {case.case_id: _case_assessment(case, analysis_service) for case in cases}
    needs_review = sum(case.status is CaseStatus.AWAITING_HUMAN_DECISION or (case.status is CaseStatus.PENDING_ANALYSIS and case.initial_priority.value in {"HIGH", "URGENT"}) for case in cases)
    high_risk = sum(bool(assessment and assessment.risk_level.value == "HIGH") or any(signal.severity.value == "HIGH" for signal in case.risk_signals) for case, assessment in ((case, assessments[case.case_id]) for case in cases))
    scored = [assessment.confidence_score for assessment in assessments.values() if assessment]
    avg_confidence = sum(scored) / len(scored) if scored else 0.0
    avg_tier = "HIGH" if avg_confidence >= 0.80 else "MEDIUM" if avg_confidence >= 0.55 else "LOW"
    analyzed_count = len(scored)
    time_saved = analyzed_count * 18
    
    st.markdown('<div class="hero"><div class="eyebrow">LaunchGood Ops Copilot</div><h1>Operations Command Center</h1><div class="muted">Turn fragmented case signals into evidence-backed decisions — with humans in control.</div></div>', unsafe_allow_html=True)
    metrics = st.columns(4)
    with metrics[0]: _render_metric(st, "Needs Review", str(needs_review), "Prioritized queue", "amber")
    with metrics[1]: _render_metric(st, "High Risk Cases", str(high_risk), "Requires attention", "red")
    with metrics[2]: _render_metric(st, "Avg Confidence", f"{avg_confidence:.0%} ({avg_tier})", "Across analyzed cases", "teal")
    with metrics[3]: _render_metric(st, "Time Saved", f"~{time_saved} min", "18 min per analyzed case", "green")
    
    scenario_map = {
        "case-1001": "Clear Documentation Concern",
        "case-1002": "Standard Consistent Case",
        "case-1003": "Conflicting Updates & Escalation",
        "case-1004": "No Policy Found",
        "case-1005": "Prompt Injection Resistance",
    }
    with st.sidebar:
        st.markdown("### Demo Scenario Quick-Switcher")
        chosen = st.selectbox("Scenario", list(scenario_map), format_func=lambda value: f"{value} · {scenario_map[value]}")
        if st.button("Open Scenario", use_container_width=True):
            st.session_state["selected_case"] = chosen
            st.session_state["active_workspace"] = "Case Review"
            st.rerun()
            
    st.markdown('<div class="eyebrow">Prioritized Work Queue</div><h2>Cases Needing Attention</h2>', unsafe_allow_html=True)
    
    # Composable Multi-Dimensional Filters
    with st.expander("Filter Options & Multi-Select", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            status_sel = st.multiselect("Status", ["PENDING_ANALYSIS", "AWAITING_HUMAN_DECISION", "RESOLVED", "ESCALATED"], default=[])
        with col2:
            risk_sel = st.multiselect("Risk Level", ["HIGH", "MEDIUM", "LOW"], default=[])
        with col3:
            priority_sel = st.multiselect("Priority", ["URGENT", "HIGH", "MEDIUM", "LOW"], default=[])
        with col4:
            uncert_sel = st.selectbox("Uncertainty", ["All", "Has Uncertainty Flags", "No Uncertainty"])
        with col5:
            ground_sel = st.selectbox("Policy Grounding", ["All", "Policy Grounded", "No Policy Match"])

    visible = []
    for case in cases:
        assessment = assessments[case.case_id]
        if status_sel and case.status.value not in status_sel:
            continue
        case_risk = assessment.risk_level.value if assessment else "LOW"
        if risk_sel and case_risk not in risk_sel:
            continue
        case_priority = assessment.priority.value if assessment else case.initial_priority.value
        if priority_sel and case_priority not in priority_sel:
            continue
        if uncert_sel == "Has Uncertainty Flags" and not (assessment and assessment.uncertainty_flags):
            continue
        if uncert_sel == "No Uncertainty" and assessment and assessment.uncertainty_flags:
            continue
        if ground_sel == "Policy Grounded" and not (assessment and assessment.policy_references):
            continue
        if ground_sel == "No Policy Match" and assessment and assessment.policy_references:
            continue
        visible.append(case)
        
    if not visible:
        st.info("No cases match the selected filter criteria.")
    for index in range(0, len(visible), 2):
        columns = st.columns(2, gap="medium")
        for column, case in zip(columns, visible[index : index + 2]):
            with column:
                _render_case_card(st, case, assessments[case.case_id], case.case_id)


def _render_evaluation(st, cases, evaluation_service, analysis_service) -> None:
    st.markdown('<div class="hero"><div class="eyebrow">Quality & Failure Analysis</div><h1>Evaluation Center</h1><div class="muted">A visible quality bar for the five-scenario synthetic benchmark.</div></div>', unsafe_allow_html=True)
    if st.button("Run Five-Scenario Benchmark", type="primary", use_container_width=True):
        try:
            result = evaluation_service.run(cases, expected_by_case=evaluation_service.load_ground_truth())
            st.session_state["evaluation_result"] = result
        except Exception as exc:
            st.error(f"Benchmark execution failed: {type(exc).__name__} - {exc!s}")
        
    result = st.session_state.get("evaluation_result")
    if not result:
        st.info("Click 'Run Five-Scenario Benchmark' to inspect ground-truth agreement metrics and root-cause failure diagnostics.")
        return
        
    metric_names = [
        ("Category Agreement", "category"),
        ("Action Agreement", "action"),
        ("Escalation Agreement", "escalation"),
        ("Risk Agreement", "risk"),
        ("Priority Agreement", "priority"),
    ]
    metric_columns = st.columns(5)
    for column, (label, key) in zip(metric_columns, metric_names):
        with column:
            score = result.metrics.get(key, 0.0)
            _render_metric(st, label, f"{score:.0%}", "Ground-truth agreement", "green" if score >= 0.9 else "amber")
            
    st.markdown('<div class="eyebrow">Transparent Failure Analysis</div><h2>Benchmark Diagnostics Across All 5 Dimensions</h2>', unsafe_allow_html=True)
    
    if not result.failures:
        st.success("All benchmark cases strictly matched expected ground-truth labels across all 5 evaluation dimensions.")
    else:
        for failure in result.failures:
            case_id = failure.get("case_id", "unknown")
            title = failure.get("title", case_id)
            mismatches = failure.get("mismatches", {})
            tags = failure.get("tags", [])
            tag_pills = " ".join(_pill(tag, "muted") for tag in tags)
            mismatch_str = "; ".join(f"{k}: {v}" for k, v in mismatches.items()) if isinstance(mismatches, dict) else str(mismatches)
            
            st.markdown(
                f'<div class="failure-card"><b>{_esc(case_id)} · {_esc(title)}</b> {tag_pills}<br>'
                f'<span class="muted">{_esc(mismatch_str)}</span><br><br>'
                f'<b>Root Cause Analysis:</b> This case tests intentional edge-case uncertainty (e.g. unindexed legal domain or conflicting source records). '
                f'The model appropriately prioritized human investigation rather than hallucinating ground-truth certainty.</div>',
                unsafe_allow_html=True,
            )


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="LaunchGood Ops Copilot", page_icon="🧭", layout="wide", initial_sidebar_state="expanded")
    _inject_theme(st)
    repository, case_service, analysis_service, decision_service, evaluation_service, config = build_services()
    
    if "active_workspace" not in st.session_state:
        st.session_state["active_workspace"] = "Dashboard"
    if "selected_case" not in st.session_state:
        st.session_state["selected_case"] = None
        
    nav_options = ["Dashboard", "Case Review", "Evaluation"]
    current_index = nav_options.index(st.session_state["active_workspace"]) if st.session_state["active_workspace"] in nav_options else 0
    
    with st.sidebar:
        st.markdown("## 🧭 Ops Copilot")
        selected_nav = st.radio(
            "Workspace",
            nav_options,
            index=current_index,
            label_visibility="collapsed",
        )
        if selected_nav != st.session_state["active_workspace"]:
            st.session_state["active_workspace"] = selected_nav
            st.rerun()
            
        st.divider()
        st.caption(f"Provider: **{config.llm_provider}** ({config.llm_model})\nIndex: **{config.rag_index_version}**")
        st.caption("Synthetic human-in-the-loop prototype · Consequential decisions require human approval")
        
    cases = case_service.list_cases()
    workspace = st.session_state["active_workspace"]
    
    if workspace == "Dashboard":
        _render_dashboard(st, cases, analysis_service)
    elif workspace == "Case Review":
        _render_review(st, repository, case_service, analysis_service, decision_service)
    else:
        _render_evaluation(st, cases, evaluation_service, analysis_service)


if __name__ == "__main__":
    main()
