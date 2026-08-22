"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Case, AIAssessment, AuditEvent } from "@/types";
import { getCaseDetails, analyzeCase, getAuditHistory, isFallbackActive } from "@/lib/api";
import DecisionRail from "@/components/DecisionRail";
import SourceTimeline from "@/components/SourceTimeline";
import AuditTimeline from "@/components/AuditTimeline";
import {
  ArrowLeft,
  Sparkles,
  ShieldAlert,
  ShieldCheck,
  FileCheck2,
  AlertTriangle,
  BookOpen,
  History,
  Layers,
  CheckCircle2,
  HelpCircle,
} from "lucide-react";
import Link from "next/link";

export default function CaseReviewPage() {
  const params = useParams();
  const router = useRouter();
  const caseId = params?.id as string;

  const [caseData, setCaseData] = useState<Case | null>(null);
  const [assessment, setAssessment] = useState<AIAssessment | null>(null);
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([]);
  const [activeTab, setActiveTab] = useState<"evidence" | "policies" | "timeline" | "uncertainty">("evidence");
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [offline, setOffline] = useState(false);

  const loadData = async () => {
    if (!caseId) return;
    try {
      const details = await getCaseDetails(caseId);
      setCaseData(details.case);
      setAssessment(details.assessment);
      setOffline(isFallbackActive());
      const audit = await getAuditHistory(caseId);
      setAuditEvents(audit.events);
    } catch (err) {
      console.error("Failed to load case data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [caseId]);

  const handleRunAnalysis = async () => {
    if (!caseId) return;
    setAnalyzing(true);
    try {
      const res = await analyzeCase(caseId);
      setCaseData(res.case);
      setAssessment(res.assessment);
      setOffline(isFallbackActive());
      const audit = await getAuditHistory(caseId);
      setAuditEvents(audit.events);
    } catch (err: any) {
      alert("Analysis failed: " + err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const isOfflineAssessment = offline || Boolean(assessment?.summary?.includes("[OFFLINE DEMO ASSESSMENT"));

  if (loading) {
    return (
      <div className="space-y-6 py-8 animate-pulse">
        <div className="h-8 w-48 bg-navy-800 rounded-lg" />
        <div className="h-44 bg-navy-900 rounded-3xl" />
        <div className="grid grid-cols-3 gap-6">
          <div className="col-span-2 h-96 bg-navy-900 rounded-3xl" />
          <div className="h-96 bg-navy-900 rounded-3xl" />
        </div>
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="text-center py-20 bg-navy-900/60 rounded-3xl border border-navy-800">
        <AlertTriangle className="w-12 h-12 text-amber-400 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-white mb-2">Case Not Found</h2>
        <p className="text-xs text-slate-400 mb-6">The requested case #{caseId} does not exist.</p>
        <Link href="/" className="inline-flex items-center gap-2 bg-brand-teal text-white text-xs font-bold px-4 py-2 rounded-xl">
          <ArrowLeft className="w-4 h-4" /> Return to Command Center
        </Link>
      </div>
    );
  }

  const riskLevel = assessment?.risk_level || (caseData.initial_priority === "HIGH" ? "HIGH" : "LOW");
  const isPending = caseData.status === "PENDING_ANALYSIS";

  return (
    <div className="space-y-8">
      {/* Back Navigation */}
      <div>
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Prioritized Queue
        </Link>
      </div>

      {/* ZONE 1: Executive Case Header */}
      <div className="relative overflow-hidden rounded-3xl bg-navy-900 border border-navy-700/80 p-7 shadow-xl">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-navy-800">
          <div className="space-y-2">
            <div className="flex items-center gap-2.5 flex-wrap">
              <span className="font-mono text-xs font-bold text-brand-tealLight bg-navy-950 px-2.5 py-1 rounded-lg border border-navy-800">
                #{caseData.case_id}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-navy-800 text-slate-300 border border-navy-700">
                {caseData.status.replace(/_/g, " ")}
              </span>
              {riskLevel === "HIGH" ? (
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-red-950/90 text-red-400 border border-red-800/80 flex items-center gap-1.5">
                  <ShieldAlert className="w-3.5 h-3.5" /> High Risk
                </span>
              ) : (
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-950/90 text-emerald-400 border border-emerald-800/80 flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5" /> Low Risk
                </span>
              )}
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">{caseData.title}</h1>
            <p className="text-xs text-slate-400 line-clamp-1 max-w-3xl">{caseData.campaign.description}</p>
          </div>

          <div>
            {isPending ? (
              <button
                onClick={handleRunAnalysis}
                disabled={analyzing}
                className="w-full sm:w-auto flex items-center justify-center gap-2.5 bg-gradient-to-r from-brand-teal to-brand-emerald hover:brightness-110 text-white font-bold text-xs py-3 px-6 rounded-xl shadow-lg shadow-brand-teal/25 transition-all disabled:opacity-50"
              >
                <Sparkles className={`w-4 h-4 ${analyzing ? "animate-spin" : ""}`} />
                <span>{analyzing ? "Running LangGraph Workflow..." : "Run AI Assessment"}</span>
              </button>
            ) : (
              <div className="flex items-center gap-2 bg-emerald-950/60 text-emerald-400 border border-emerald-800/60 px-4 py-2 rounded-xl text-xs font-semibold">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>AI Assessment Complete</span>
              </div>
            )}
          </div>
        </div>

        {/* Executive Metrics Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 pt-6">
          <div className="bg-navy-950/60 rounded-xl p-3.5 border border-navy-800">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Category</span>
            <div className="text-xs font-bold text-white mt-1 truncate">
              {assessment ? assessment.category.replace(/_/g, " ") : caseData.intake_category.replace(/_/g, " ")}
            </div>
          </div>

          <div className="bg-navy-950/60 rounded-xl p-3.5 border border-navy-800">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Assessed Risk</span>
            <div className={`text-xs font-bold mt-1 ${riskLevel === "HIGH" ? "text-red-400" : "text-emerald-400"}`}>
              {assessment ? assessment.risk_level : "PENDING"}
            </div>
          </div>

          <div className="bg-navy-950/60 rounded-xl p-3.5 border border-navy-800">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Priority</span>
            <div className="text-xs font-bold text-white mt-1">
              {assessment ? assessment.priority : caseData.initial_priority}
            </div>
          </div>

          <div className="bg-navy-950/60 rounded-xl p-3.5 border border-navy-800">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Confidence</span>
              <HelpCircle className="w-3 h-3 text-slate-500" />
            </div>
            <div className="text-xs font-bold text-brand-tealLight mt-1">
              {assessment ? `${Math.round(assessment.confidence_score * 100)}% (${assessment.confidence_tier})` : "—"}
            </div>
          </div>

          <div className="bg-navy-950/60 rounded-xl p-3.5 border border-navy-800 col-span-2 sm:col-span-1">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">AI Recommendation</span>
            <div className="text-xs font-bold text-white mt-1 truncate">
              {assessment ? assessment.recommendation_action.replace(/_/g, " ") : "—"}
            </div>
          </div>
        </div>
      </div>

      {/* Main Review Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* ZONE 2: Tabbed Evidence & Context Workspace */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-navy-900/90 rounded-2xl border border-navy-700 p-6 shadow-xl">
            {/* Workspace Tabs */}
            <div className="flex items-center gap-2 pb-4 mb-6 border-b border-navy-800 overflow-x-auto">
              {[
                { id: "evidence", label: `Evidence (${assessment?.evidence.length || 0})`, icon: FileCheck2 },
                { id: "policies", label: `Retrieved Policies (${assessment?.policy_references.length || 0})`, icon: BookOpen },
                { id: "timeline", label: "Source Timeline", icon: Layers },
                {
                  id: "uncertainty",
                  label: `Uncertainty & Conflicts (${assessment?.uncertainty_flags.length || 0})`,
                  icon: AlertTriangle,
                },
              ].map((tab) => {
                const Icon = tab.icon;
                const active = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                      active
                        ? "bg-brand-teal text-white shadow-md shadow-brand-teal/20"
                        : "text-slate-400 hover:text-white hover:bg-navy-800"
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>

            {/* TAB CONTENT: Evidence & Grounding */}
            {activeTab === "evidence" && (
              <div className="space-y-4">
                {!assessment || assessment.evidence.length === 0 ? (
                  <div className="text-center py-12 text-slate-400 text-xs">
                    No evidence extracted yet. Run the AI assessment above.
                  </div>
                ) : (
                  assessment.evidence.map((item) => (
                    <div key={item.evidence_id} className="bg-navy-950/80 rounded-xl p-4 border border-navy-800 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-brand-teal/20 text-brand-tealLight border border-brand-teal/30">
                          Supports {item.supports}
                        </span>
                        <span className="font-mono text-[10px] text-slate-400 bg-navy-900 px-2 py-0.5 rounded border border-navy-800">
                          Source: {item.source_id}
                        </span>
                      </div>
                      <p className="text-xs text-slate-200 leading-relaxed font-medium">"{item.fact}"</p>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* TAB CONTENT: Retrieved Policies */}
            {activeTab === "policies" && (
              <div className="space-y-4">
                {!assessment || assessment.policy_references.length === 0 ? (
                  <div className="text-center py-12 text-slate-400 text-xs">
                    No policy references retrieved. The query may have fallen below similarity thresholds.
                  </div>
                ) : (
                  assessment.policy_references.map((pol) => (
                    <div key={pol.chunk_id} className="bg-navy-950/80 rounded-xl p-5 border border-navy-800 space-y-3">
                      <div className="flex items-center justify-between flex-wrap gap-2">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-white bg-navy-900 px-2.5 py-1 rounded border border-navy-700">
                            {pol.policy_id}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">Chunk: {pol.chunk_id}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                              pol.grounding_status === "STRONG"
                                ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                                : "bg-amber-950 text-amber-400 border border-amber-800"
                            }`}
                          >
                            {pol.grounding_status} Grounding
                          </span>
                          <span className="text-[10px] font-mono text-slate-400">Score: {pol.retrieval_score.toFixed(3)}</span>
                        </div>
                      </div>
                      <div className="p-3 bg-navy-900/60 rounded-lg border border-navy-800/80 text-xs text-slate-300 font-mono leading-relaxed">
                        {pol.excerpt}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* TAB CONTENT: Source Timeline */}
            {activeTab === "timeline" && <SourceTimeline caseData={caseData} />}

            {/* TAB CONTENT: Uncertainty & Conflicts */}
            {activeTab === "uncertainty" && (
              <div className="space-y-4">
                {!assessment || assessment.uncertainty_flags.length === 0 ? (
                  <div className="flex items-center gap-3 p-4 rounded-xl bg-emerald-950/40 border border-emerald-800/50 text-emerald-400 text-xs">
                    <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                    <span>No conflicting facts or policy grounding gaps detected in this case.</span>
                  </div>
                ) : (
                  assessment.uncertainty_flags.map((flag, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-4 rounded-xl bg-amber-950/40 border border-amber-800/60 text-amber-300 text-xs">
                      <AlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-400 mt-0.5" />
                      <div>
                        <span className="font-bold text-amber-200">Uncertainty Trigger: {flag.replace(/_/g, " ")}</span>
                        <p className="text-[11px] text-amber-300/80 mt-1">
                          The system reduced its confidence score and elevated this case for mandatory human verification.
                        </p>
                      </div>
                    </div>
                  ))
                )}

                {assessment?.escalation_recommended && (
                  <div className="flex items-start gap-3 p-4 rounded-xl bg-red-950/40 border border-red-800/60 text-red-300 text-xs">
                    <ShieldAlert className="w-5 h-5 flex-shrink-0 text-red-400 mt-0.5" />
                    <div>
                      <span className="font-bold text-red-200">Mandatory Lead Escalation Recommended</span>
                      <p className="text-[11px] text-red-300/80 mt-1">
                        Contradictory records or policy ambiguity requires operations lead review before campaign disbursement.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* ZONE 4: Visual Audit History */}
          <AuditTimeline events={auditEvents} />
        </div>

        {/* ZONE 3: Persistent Human Decision Rail */}
        <div className="lg:col-span-1">
          <DecisionRail caseData={caseData} assessment={assessment} onDecisionSubmitted={loadData} />
        </div>
      </div>
    </div>
  );
}
