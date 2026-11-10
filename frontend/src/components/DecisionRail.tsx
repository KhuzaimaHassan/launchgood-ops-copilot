"use client";

import { useState } from "react";
import { Case, AIAssessment, DecisionType, ReviewerDecision } from "@/types";
import { submitDecision } from "@/lib/api";
import { CheckCircle, AlertOctagon, CornerDownRight, XCircle, ArrowUpRight, Check } from "lucide-react";

interface DecisionRailProps {
  caseData: Case;
  assessment: AIAssessment | null;
  decisions: ReviewerDecision[];
  offline: boolean;
  onDecisionSubmitted: (decision: ReviewerDecision) => Promise<void>;
}

export default function DecisionRail({ caseData, assessment, decisions, offline, onDecisionSubmitted }: DecisionRailProps) {
  const [decisionType, setDecisionType] = useState<DecisionType>("APPROVE");
  const [overriddenRisk, setOverriddenRisk] = useState<string>("UNCHANGED");
  const [overriddenPriority, setOverriddenPriority] = useState<string>("UNCHANGED");
  const [overriddenRec, setOverriddenRec] = useState<string>("");
  const [reviewerNotes, setReviewerNotes] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit || isSubmitting) return;
    setIsSubmitting(true);
    setSuccessMsg(null);
    setErrorMsg(null);
    try {
      const saved = await submitDecision(caseData.case_id, {
        decision_type: decisionType,
        overridden_risk: overriddenRisk === "UNCHANGED" ? null : overriddenRisk,
        overridden_priority: overriddenPriority === "UNCHANGED" ? null : overriddenPriority,
        overridden_recommendation: overriddenRec.trim() || null,
        reviewer_notes: reviewerNotes.trim() || null,
        reviewer_id: "human-reviewer-01",
      });
      setSuccessMsg("Decision recorded successfully.");
      await onDecisionSubmitted(saved);
    } catch (err: any) {
      setErrorMsg(err.message || "Decision submission failed. Consequential decisions require backend persistence.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const isAnalyzed = Boolean(assessment);
  const recorded = decisions[decisions.length - 1];
  const isClosed = caseData.status === "RESOLVED" || caseData.status === "ESCALATED";
  const canSubmit = isAnalyzed && !offline && !isClosed && !recorded && caseData.status === "AWAITING_HUMAN_DECISION";

  return (
    <div className="bg-navy-900/95 rounded-2xl border border-navy-700 p-6 shadow-xl sticky top-24">
      <div className="flex items-center justify-between pb-4 mb-5 border-b border-navy-800">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-brand-tealLight">Human Control</span>
          <h3 className="text-base font-bold text-white">Decision Rail</h3>
        </div>
        <div className="text-right">
          <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-navy-800 text-slate-300 border border-navy-700">
            Reviewer Mode
          </span>
        </div>
      </div>

      {recorded ? (
        <section aria-label="Recorded human decision" className="space-y-4 text-xs break-words">
          <div className="rounded-xl p-4 bg-emerald-950/40 border border-emerald-800/60">
            <h4 className="font-bold text-emerald-300">Recorded Human Decision: {recorded.decision_type}</h4>
            <p className="mt-1 text-slate-300">Case {caseData.status.replace(/_/g, " ")}. Further submission is closed.</p>
          </div>
          <dl className="space-y-3">
            <div><dt className="text-slate-400">Final risk</dt><dd className="text-white mt-1">{recorded.overridden_risk ?? assessment?.risk_level ?? "Not available"}{recorded.overridden_risk ? " (reviewer override)" : " (AI unchanged)"}</dd></div>
            <div><dt className="text-slate-400">Final priority</dt><dd className="text-white mt-1">{recorded.overridden_priority ?? assessment?.priority ?? "Not available"}{recorded.overridden_priority ? " (reviewer override)" : " (AI unchanged)"}</dd></div>
            <div><dt className="text-slate-400">Final recommendation</dt><dd className="text-white mt-1 whitespace-pre-wrap">{recorded.overridden_recommendation ?? assessment?.recommendation_action.replace(/_/g, " ") ?? "Not available"}</dd></div>
            <div><dt className="text-slate-400">Reviewer notes & rationale</dt><dd className="text-white mt-1 whitespace-pre-wrap">{recorded.reviewer_notes || "No notes recorded."}</dd></div>
            <div><dt className="text-slate-400">Reviewer</dt><dd className="text-white mt-1">{recorded.reviewer_id}</dd></div>
            <div><dt className="text-slate-400">Recorded at</dt><dd className="text-white mt-1">{recorded.created_at ? new Date(recorded.created_at).toLocaleString() : "Not available"}</dd></div>
          </dl>
          <p className="text-slate-400">The original AI assessment remains unchanged above.</p>
        </section>
      ) : isClosed ? (
        <p role="status" className="text-xs text-amber-300 leading-relaxed">This case is {caseData.status.toLowerCase()}; further submission is closed. Recorded decision details are unavailable from the connected API.</p>
      ) : offline ? (
        <p role="status" className="text-xs text-amber-300 leading-relaxed">Offline preview only. Connect to the backend before recording a human decision.</p>
      ) : !isAnalyzed ? (
        <div className="bg-navy-950/60 rounded-xl p-5 border border-navy-800 text-center">
          <AlertOctagon className="w-8 h-8 text-amber-400 mx-auto mb-2 opacity-80" />
          <p className="text-xs font-semibold text-slate-200 mb-1">Assessment Required</p>
          <p className="text-[11px] text-slate-400">
            Run the AI assessment above before recording a consequential human decision.
          </p>
        </div>
      ) : !canSubmit ? (
        <p role="status" className="text-xs text-amber-300">A decision can only be recorded while this case is awaiting human decision.</p>
      ) : (
        <form onSubmit={handleSubmit}>
          <fieldset disabled={isSubmitting} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-300 mb-1.5">Consequential Action</label>
            <div className="grid grid-cols-2 gap-2">
              {[
                { type: "APPROVE", label: "Approve", icon: CheckCircle, color: "hover:border-emerald-500" },
                { type: "MODIFY", label: "Modify", icon: CornerDownRight, color: "hover:border-blue-500" },
                { type: "REJECT", label: "Reject", icon: XCircle, color: "hover:border-red-500" },
                { type: "ESCALATE", label: "Escalate", icon: ArrowUpRight, color: "hover:border-purple-500" },
              ].map((item) => {
                const Icon = item.icon;
                const active = decisionType === item.type;
                return (
                  <button
                    key={item.type}
                    type="button"
                    aria-pressed={active}
                    onClick={() => setDecisionType(item.type as DecisionType)}
                    className={`flex items-center gap-2 p-2.5 rounded-xl border text-xs font-bold transition-all ${
                      active
                        ? "bg-brand-teal text-white border-brand-tealLight shadow-md shadow-brand-teal/20"
                        : `bg-navy-950/60 text-slate-300 border-navy-700 ${item.color}`
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label htmlFor="risk-override" className="block text-[11px] font-semibold text-slate-400 mb-1">Risk Override</label>
              <select id="risk-override"
                value={overriddenRisk}
                onChange={(e) => setOverriddenRisk(e.target.value)}
                className="w-full bg-navy-950 border border-navy-700 text-white rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-brand-teal"
              >
                <option value="UNCHANGED">Unchanged ({assessment?.risk_level})</option>
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
              </select>
            </div>

            <div>
              <label htmlFor="priority-override" className="block text-[11px] font-semibold text-slate-400 mb-1">Priority Override</label>
              <select id="priority-override"
                value={overriddenPriority}
                onChange={(e) => setOverriddenPriority(e.target.value)}
                className="w-full bg-navy-950 border border-navy-700 text-white rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-brand-teal"
              >
                <option value="UNCHANGED">Unchanged ({assessment?.priority})</option>
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
                <option value="URGENT">Urgent</option>
              </select>
            </div>
          </div>

          <div>
            <label htmlFor="recommendation-override" className="block text-[11px] font-semibold text-slate-400 mb-1">Recommendation Override (Optional)</label>
            <input id="recommendation-override"
              type="text"
              placeholder="e.g. Request hospital invoice discharge certificate..."
              value={overriddenRec}
              onChange={(e) => setOverriddenRec(e.target.value)}
              className="w-full bg-navy-950 border border-navy-700 text-white rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-brand-teal placeholder:text-slate-600"
            />
          </div>

          <div>
            <label htmlFor="reviewer-notes" className="block text-[11px] font-semibold text-slate-400 mb-1">Reviewer Notes & Rationale</label>
            <textarea id="reviewer-notes"
              rows={3}
              placeholder="Document the operational basis for your final decision..."
              value={reviewerNotes}
              onChange={(e) => setReviewerNotes(e.target.value)}
              className="w-full bg-navy-950 border border-navy-700 text-white rounded-lg p-2.5 text-xs focus:outline-none focus:border-brand-teal placeholder:text-slate-600 resize-none"
            />
          </div>

          {successMsg && (
            <div className="flex items-center gap-2 p-2.5 rounded-lg bg-emerald-950/80 border border-emerald-800/80 text-emerald-400 text-xs font-semibold">
              <Check className="w-4 h-4 flex-shrink-0" />
              <span>{successMsg}</span>
            </div>
          )}

          {errorMsg && (
            <div className="flex items-start gap-2 p-3 rounded-xl bg-red-950/90 border border-red-800/90 text-red-300 text-xs font-semibold leading-relaxed shadow-lg">
              <AlertOctagon className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-gradient-to-r from-brand-teal to-brand-emerald hover:brightness-110 text-white font-bold py-3 px-4 rounded-xl text-xs shadow-lg shadow-brand-teal/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isSubmitting ? "Recording Decision..." : "Submit Consequential Decision"}
          </button>
          </fieldset>
        </form>
      )}
    </div>
  );
}
