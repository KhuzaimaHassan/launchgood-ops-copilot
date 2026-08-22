import Link from "next/link";
import { Case, AIAssessment } from "@/types";
import { ArrowRight, AlertTriangle, ShieldCheck, FileText } from "lucide-react";

interface CaseCardProps {
  caseData: Case;
  assessment?: AIAssessment | null;
}

export default function CaseCard({ caseData, assessment }: CaseCardProps) {
  const isHighRisk = assessment
    ? assessment.risk_level === "HIGH"
    : caseData.initial_priority === "HIGH" || caseData.initial_priority === "URGENT" || caseData.risk_signals.some((s) => s.severity === "HIGH");

  const isPending = caseData.status === "PENDING_ANALYSIS";
  const isAwaiting = caseData.status === "AWAITING_HUMAN_DECISION";
  const isResolved = caseData.status === "RESOLVED";

  const riskBadge = isHighRisk ? (
    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-red-950/80 text-red-400 border border-red-800/80 flex items-center gap-1">
      <AlertTriangle className="w-3 h-3" /> Risk: {assessment ? assessment.risk_level : "HIGH"}
    </span>
  ) : (
    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-950/80 text-emerald-400 border border-emerald-800/80 flex items-center gap-1">
      <ShieldCheck className="w-3 h-3" /> Risk: {assessment ? assessment.risk_level : "LOW"}
    </span>
  );

  const statusBadge = isPending ? (
    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-amber-950/60 text-amber-300 border border-amber-800/60">
      Pending Analysis
    </span>
  ) : isAwaiting ? (
    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-brand-teal/20 text-brand-tealLight border border-brand-teal/40">
      Awaiting Decision
    </span>
  ) : isResolved ? (
    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-950/60 text-emerald-300 border border-emerald-800/60">
      Resolved
    </span>
  ) : (
    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-purple-950/60 text-purple-300 border border-purple-800/60">
      Escalated
    </span>
  );

  const confBadge = assessment ? (
    <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
      assessment.confidence_tier === "HIGH"
        ? "bg-brand-teal/20 text-brand-tealLight border border-brand-teal/30"
        : "bg-amber-950/60 text-amber-300 border border-amber-800/60"
    }`}>
      Conf: {Math.round(assessment.confidence_score * 100)}% ({assessment.confidence_tier})
    </span>
  ) : (
    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-navy-800 text-slate-400 border border-navy-700">
      Conf: Not Analyzed
    </span>
  );

  const policyTag = assessment
    ? assessment.policy_references.length > 0
      ? <span className="text-emerald-400">Policy Grounded</span>
      : <span className="text-amber-400">No Policy Match</span>
    : <span className="text-slate-500">No Policy Yet</span>;

  return (
    <div className="bg-navy-900/90 hover:bg-navy-850 rounded-2xl p-6 border border-navy-700 hover:border-brand-teal/50 transition-all duration-200 shadow-lg shadow-navy-950/40 flex flex-col justify-between group">
      <div>
        <div className="flex items-center justify-between gap-2 mb-3 flex-wrap">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-mono text-xs font-bold text-brand-tealLight bg-navy-800 px-2 py-0.5 rounded-md border border-navy-700">
              #{caseData.case_id}
            </span>
            {riskBadge}
            {confBadge}
          </div>
          {statusBadge}
        </div>

        <h3 className="text-base font-bold text-white group-hover:text-brand-tealLight transition-colors line-clamp-1 mb-1.5">
          {caseData.title}
        </h3>

        <p className="text-xs text-slate-400 line-clamp-2 mb-4 leading-relaxed">
          {assessment ? (assessment.summary || assessment.recommendation_rationale) : caseData.campaign.description}
        </p>
      </div>

      <div>
        <div className="flex items-center gap-3 pt-3 border-t border-navy-800 text-[11px] text-slate-400 mb-4 flex-wrap">
          <span className="flex items-center gap-1">
            <FileText className="w-3.5 h-3.5 text-slate-500" />
            {caseData.support_messages.length + caseData.campaign_updates.length} records
          </span>
          <span>•</span>
          <span className="truncate">{caseData.intake_category.replace(/_/g, " ")}</span>
          <span>•</span>
          <span className="font-medium text-slate-300">
            {assessment ? `Initial: ${caseData.initial_priority} | AI: ${assessment.priority}` : `Initial: ${caseData.initial_priority}`}
          </span>
          <span>•</span>
          {policyTag}
        </div>

        <Link
          href={`/cases/${caseData.case_id}`}
          className="w-full flex items-center justify-center gap-2 bg-navy-800 hover:bg-brand-teal text-white text-xs font-bold py-2.5 px-4 rounded-xl border border-navy-700 hover:border-brand-tealLight transition-all duration-150"
        >
          <span>Review Case</span>
          <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
        </Link>
      </div>
    </div>
  );
}
