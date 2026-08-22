"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ShieldCheck, Activity, ChevronDown, Compass, CheckCircle2, AlertTriangle } from "lucide-react";
import { useEffect, useState } from "react";
import { checkHealth } from "@/lib/api";

const DEMO_SCENARIOS = [
  { id: "case-1001", label: "Case #1001 · Missing Medical Docs" },
  { id: "case-1002", label: "Case #1002 · Standard Food Drive" },
  { id: "case-1003", label: "Case #1003 · Conflicting Updates" },
  { id: "case-1004", label: "Case #1004 · No Applicable Policy" },
  { id: "case-1005", label: "Case #1005 · Misleading Text Test" },
];

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking");

  useEffect(() => {
    checkHealth().then((res) => {
      setBackendStatus(res.status === "ok" ? "online" : "offline");
    });
  }, []);

  return (
    <header className="sticky top-0 z-50 bg-navy-950/90 backdrop-blur-md border-b border-navy-700/60 px-4 sm:px-6 py-3">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
        {/* Brand & Nav */}
        <div className="flex items-center justify-between gap-4">
          <Link href="/" className="flex items-center gap-2.5 sm:gap-3 group shrink-0">
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-brand-teal to-brand-emerald flex items-center justify-center shadow-lg shadow-brand-teal/20 group-hover:scale-105 transition-transform shrink-0">
              <Compass className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap">
                <span className="font-extrabold text-base sm:text-lg tracking-tight text-white">LaunchGood</span>
                <span className="text-[10px] sm:text-xs font-semibold px-2 py-0.5 rounded-full bg-brand-teal/20 text-brand-tealLight border border-brand-teal/30 whitespace-nowrap">
                  Ops Copilot
                </span>
              </div>
              <p className="text-[10px] sm:text-[11px] text-slate-400 font-medium hidden sm:block">
                Human-in-the-Loop Operations Command
              </p>
            </div>
          </Link>

          {/* Connection status badge (Visible on mobile top-right) */}
          <div className="md:hidden">
            <div
              className={`flex items-center gap-1.5 text-[11px] font-medium px-2.5 py-1 rounded-full border ${
                backendStatus === "online"
                  ? "bg-emerald-950/60 text-emerald-400 border-emerald-800/60"
                  : backendStatus === "offline"
                  ? "bg-amber-950/60 text-amber-400 border-amber-800/60"
                  : "bg-navy-800 text-slate-400 border-navy-700"
              }`}
            >
              <span
                className={`w-1.5 h-1.5 rounded-full ${
                  backendStatus === "online"
                    ? "bg-emerald-400 animate-pulse"
                    : backendStatus === "offline"
                    ? "bg-amber-400"
                    : "bg-slate-500"
                }`}
              />
              <span>{backendStatus === "online" ? "FastAPI Online" : backendStatus === "offline" ? "Demo Mode" : "Connecting..."}</span>
            </div>
          </div>
        </div>

        {/* Navigation & Controls */}
        <div className="flex items-center justify-between sm:justify-end gap-2 sm:gap-3 flex-wrap">
          <nav className="flex items-center gap-1 bg-navy-900/90 p-1 rounded-xl border border-navy-700 w-full sm:w-auto justify-center">
            <Link
              href="/"
              className={`px-3 sm:px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors text-center flex-1 sm:flex-none ${
                pathname === "/"
                  ? "bg-brand-teal text-white shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-navy-800"
              }`}
            >
              Command Center
            </Link>
            <Link
              href="/evaluation"
              className={`px-3 sm:px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors text-center flex-1 sm:flex-none ${
                pathname.startsWith("/evaluation")
                  ? "bg-brand-teal text-white shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-navy-800"
              }`}
            >
              Evaluation & Benchmarks
            </Link>
          </nav>

          <div className="flex items-center gap-2 w-full sm:w-auto justify-between sm:justify-start">
            <div className="flex items-center gap-1.5 bg-navy-900 px-2.5 py-1 rounded-lg border border-navy-700 text-xs flex-1 sm:flex-none">
              <span className="text-slate-400 hidden xl:inline">Quick Scenario:</span>
              <select
                className="bg-transparent text-white font-medium focus:outline-none cursor-pointer w-full text-xs"
                onChange={(e) => {
                  if (e.target.value) {
                    router.push(`/cases/${e.target.value}`);
                  }
                }}
                defaultValue=""
              >
                <option value="" disabled className="bg-navy-900 text-slate-400">Select Demo Preset...</option>
                {DEMO_SCENARIOS.map((s) => (
                  <option key={s.id} value={s.id} className="bg-navy-900 text-white">
                    {s.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Connection status badge (Desktop/Tablet) */}
            <div className="hidden md:flex">
              <div
                className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-full border whitespace-nowrap ${
                  backendStatus === "online"
                    ? "bg-emerald-950/60 text-emerald-400 border-emerald-800/60"
                    : backendStatus === "offline"
                    ? "bg-amber-950/60 text-amber-400 border-amber-800/60"
                    : "bg-navy-800 text-slate-400 border-navy-700"
                }`}
              >
                <span
                  className={`w-2 h-2 rounded-full ${
                    backendStatus === "online"
                      ? "bg-emerald-400 animate-pulse"
                      : backendStatus === "offline"
                      ? "bg-amber-400"
                      : "bg-slate-500"
                  }`}
                />
                <span>{backendStatus === "online" ? "FastAPI Online" : backendStatus === "offline" ? "Demo Mode (Mock)" : "Connecting..."}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
