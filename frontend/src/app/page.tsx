"use client";

import { useEffect, useState } from "react";
import { Case, AIAssessment } from "@/types";
import { getCases, getCaseDetails, isFallbackActive } from "@/lib/api";
import MetricCard from "@/components/MetricCard";
import CaseCard from "@/components/CaseCard";
import { ShieldAlert, Inbox, CheckCircle2, Clock, Sparkles, Filter, X, AlertTriangle } from "lucide-react";

export default function DashboardPage() {
  const [cases, setCases] = useState<Case[]>([]);
  const [assessments, setAssessments] = useState<Record<string, AIAssessment | null>>({});
  const [loading, setLoading] = useState(true);
  const [fallbackActive, setFallbackActive] = useState(false);

  // Multi-dimensional composable filters
  const [selectedStatuses, setSelectedStatuses] = useState<string[]>([]);
  const [selectedRisks, setSelectedRisks] = useState<string[]>([]);
  const [selectedPriorities, setSelectedPriorities] = useState<string[]>([]);
  const [uncertaintyFilter, setUncertaintyFilter] = useState<"ALL" | "HAS_UNCERTAINTY" | "NO_UNCERTAINTY">("ALL");
  const [groundingFilter, setGroundingFilter] = useState<"ALL" | "GROUNDED" | "NO_MATCH">("ALL");

  useEffect(() => {
    async function loadData() {
      try {
        const fetchedCases = await getCases();
        setCases(fetchedCases);
        setFallbackActive(isFallbackActive());
        const map: Record<string, AIAssessment | null> = {};
        for (const c of fetchedCases) {
          try {
            const details = await getCaseDetails(c.case_id);
            map[c.case_id] = details.assessment;
          } catch {
            map[c.case_id] = null;
          }
        }
        setAssessments(map);
      } catch (err) {
        console.error("Error loading dashboard data:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const needsReviewCount = cases.filter(
    (c) => c.status === "AWAITING_HUMAN_DECISION" || (c.status === "PENDING_ANALYSIS" && (c.initial_priority === "HIGH" || c.initial_priority === "URGENT"))
  ).length;

  const highRiskCount = cases.filter((c) => {
    const asm = assessments[c.case_id];
    return (asm && asm.risk_level === "HIGH") || c.initial_priority === "HIGH" || c.initial_priority === "URGENT" || c.risk_signals.some((s) => s.severity === "HIGH");
  }).length;

  const scoredAssessments = Object.values(assessments).filter((a): a is AIAssessment => a !== null);
  const avgConfidence = scoredAssessments.length
    ? scoredAssessments.reduce((acc, a) => acc + a.confidence_score, 0) / scoredAssessments.length
    : 0;
  const avgTier = avgConfidence >= 0.8 ? "HIGH" : avgConfidence >= 0.55 ? "MEDIUM" : "LOW";
  const timeSavedMinutes = scoredAssessments.length * 18;

  const toggleArrayFilter = (arr: string[], val: string, setter: (newArr: string[]) => void) => {
    if (arr.includes(val)) {
      setter(arr.filter((item) => item !== val));
    } else {
      setter([...arr, val]);
    }
  };

  const clearAllFilters = () => {
    setSelectedStatuses([]);
    setSelectedRisks([]);
    setSelectedPriorities([]);
    setUncertaintyFilter("ALL");
    setGroundingFilter("ALL");
  };

  const hasActiveFilters =
    selectedStatuses.length > 0 ||
    selectedRisks.length > 0 ||
    selectedPriorities.length > 0 ||
    uncertaintyFilter !== "ALL" ||
    groundingFilter !== "ALL";

  const filteredCases = cases.filter((c) => {
    const asm = assessments[c.case_id];
    if (selectedStatuses.length > 0 && !selectedStatuses.includes(c.status)) return false;
    
    const riskLevel = asm ? asm.risk_level : c.initial_priority === "HIGH" ? "HIGH" : "LOW";
    if (selectedRisks.length > 0 && !selectedRisks.includes(riskLevel)) return false;

    const priorityLevel = asm ? asm.priority : c.initial_priority;
    if (selectedPriorities.length > 0 && !selectedPriorities.includes(priorityLevel)) return false;

    if (uncertaintyFilter === "HAS_UNCERTAINTY" && !(asm && asm.uncertainty_flags.length > 0)) return false;
    if (uncertaintyFilter === "NO_UNCERTAINTY" && asm && asm.uncertainty_flags.length > 0) return false;

    if (groundingFilter === "GROUNDED" && !(asm && asm.policy_references.length > 0)) return false;
    if (groundingFilter === "NO_MATCH" && asm && asm.policy_references.length > 0) return false;

    return true;
  });

  return (
    <div className="space-y-8">
      {fallbackActive && (
        <div className="flex items-center gap-3 p-4 rounded-2xl bg-amber-950/80 border border-amber-800/80 text-amber-300 text-xs font-semibold shadow-lg">
          <AlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-400" />
          <span>
            <b>Offline Demo Mode Active:</b> FastAPI backend (<code>http://localhost:8000</code>) is unreachable. Displaying fallback synthetic dataset. Start FastAPI to enable live database persistence.
          </span>
        </div>
      )}

      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900 border border-navy-700/80 p-8 shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-teal/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />
        <div className="relative z-10 max-w-3xl">
          <div className="flex items-center gap-2 text-brand-tealLight text-xs font-bold uppercase tracking-wider mb-2">
            <Sparkles className="w-4 h-4" /> Operations Command Center
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-3">
            Evidence-Backed Campaign Operations
          </h1>
          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            Synthesize campaign details, support messages, updates, and risk signals against verified LaunchGood compliance policies. AI prepares the structured assessment — human reviewers own the consequence.
          </p>
        </div>
      </div>

      {/* KPI Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label="Needs Review"
          value={needsReviewCount}
          note="Active reviewer queue"
          icon={<Inbox className="w-5 h-5" />}
          tone="amber"
        />
        <MetricCard
          label="High Risk Cases"
          value={highRiskCount}
          note="Requires attention"
          icon={<ShieldAlert className="w-5 h-5" />}
          tone="red"
        />
        <MetricCard
          label="Avg Confidence"
          value={`${Math.round(avgConfidence * 100)}% (${avgTier})`}
          note="Across analyzed cases"
          icon={<CheckCircle2 className="w-5 h-5" />}
          tone="teal"
        />
        <MetricCard
          label="Est. Time Saved"
          value={`~${timeSavedMinutes} min`}
          note="18 min average per case"
          icon={<Clock className="w-5 h-5" />}
          tone="green"
        />
      </div>

      {/* Work Queue & Composable Multi-Dimensional Filters */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">Prioritized Case Queue</h2>
            <p className="text-xs text-slate-400">Multi-dimensional composable filtering by Status, Risk, Priority, Uncertainty, and Policy Grounding.</p>
          </div>

          {hasActiveFilters && (
            <button
              onClick={clearAllFilters}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-amber-400 hover:text-amber-300 bg-amber-950/60 px-3 py-1.5 rounded-xl border border-amber-800/60 self-start sm:self-auto"
            >
              <X className="w-3.5 h-3.5" /> Clear Active Filters
            </button>
          )}
        </div>

        {/* Composable Filter Bar */}
        <div className="bg-navy-900/90 rounded-2xl p-5 border border-navy-700 space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-300">
            <Filter className="w-4 h-4 text-brand-tealLight" /> Composable Filters
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Status Filter */}
            <div>
              <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Lifecycle Status</span>
              <div className="flex flex-wrap gap-1">
                {["PENDING_ANALYSIS", "AWAITING_HUMAN_DECISION", "RESOLVED", "ESCALATED"].map((st) => (
                  <button
                    key={st}
                    onClick={() => toggleArrayFilter(selectedStatuses, st, setSelectedStatuses)}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-colors ${
                      selectedStatuses.includes(st)
                        ? "bg-brand-teal text-white border border-brand-tealLight"
                        : "bg-navy-950 text-slate-400 border border-navy-800 hover:text-white"
                    }`}
                  >
                    {st.replace(/_/g, " ")}
                  </button>
                ))}
              </div>
            </div>

            {/* Risk Filter */}
            <div>
              <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Risk Level</span>
              <div className="flex flex-wrap gap-1">
                {["HIGH", "MEDIUM", "LOW"].map((rk) => (
                  <button
                    key={rk}
                    onClick={() => toggleArrayFilter(selectedRisks, rk, setSelectedRisks)}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-colors ${
                      selectedRisks.includes(rk)
                        ? "bg-brand-teal text-white border border-brand-tealLight"
                        : "bg-navy-950 text-slate-400 border border-navy-800 hover:text-white"
                    }`}
                  >
                    {rk}
                  </button>
                ))}
              </div>
            </div>

            {/* Priority Filter */}
            <div>
              <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Priority</span>
              <div className="flex flex-wrap gap-1">
                {["URGENT", "HIGH", "MEDIUM", "LOW"].map((pr) => (
                  <button
                    key={pr}
                    onClick={() => toggleArrayFilter(selectedPriorities, pr, setSelectedPriorities)}
                    className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-colors ${
                      selectedPriorities.includes(pr)
                        ? "bg-brand-teal text-white border border-brand-tealLight"
                        : "bg-navy-950 text-slate-400 border border-navy-800 hover:text-white"
                    }`}
                  >
                    {pr}
                  </button>
                ))}
              </div>
            </div>

            {/* Uncertainty & Grounding Dropdowns */}
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Uncertainty</span>
                <select
                  value={uncertaintyFilter}
                  onChange={(e) => setUncertaintyFilter(e.target.value as any)}
                  className="w-full bg-navy-950 border border-navy-800 text-white rounded-lg p-1.5 text-xs focus:outline-none focus:border-brand-teal"
                >
                  <option value="ALL">All</option>
                  <option value="HAS_UNCERTAINTY">Has Flags</option>
                  <option value="NO_UNCERTAINTY">No Flags</option>
                </select>
              </div>

              <div>
                <span className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Grounding</span>
                <select
                  value={groundingFilter}
                  onChange={(e) => setGroundingFilter(e.target.value as any)}
                  className="w-full bg-navy-950 border border-navy-800 text-white rounded-lg p-1.5 text-xs focus:outline-none focus:border-brand-teal"
                >
                  <option value="ALL">All</option>
                  <option value="GROUNDED">Policy Grounded</option>
                  <option value="NO_MATCH">No Policy Match</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 py-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-48 rounded-2xl bg-navy-900/60 border border-navy-800 animate-pulse" />
            ))}
          </div>
        ) : filteredCases.length === 0 ? (
          <div className="text-center py-16 bg-navy-900/40 rounded-2xl border border-navy-800">
            <Inbox className="w-12 h-12 text-slate-600 mx-auto mb-3" />
            <h3 className="text-sm font-bold text-white mb-1">No cases match the active filter criteria</h3>
            <p className="text-xs text-slate-400">Adjust the composable filter bar or click 'Clear Active Filters'.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredCases.map((c) => (
              <CaseCard key={c.case_id} caseData={c} assessment={assessments[c.case_id]} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
