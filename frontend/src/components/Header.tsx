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
    <header className="sticky top-0 z-50 bg-navy-950/80 backdrop-blur-md border-b border-navy-700/60 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-teal to-brand-emerald flex items-center justify-center shadow-lg shadow-brand-teal/20 group-hover:scale-105 transition-transform">
              <Compass className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight text-white">LaunchGood</span>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-brand-teal/20 text-brand-tealLight border border-brand-teal/30">
                  Ops Copilot
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">Human-in-the-Loop Operations Command</p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1 bg-navy-900/90 p-1 rounded-xl border border-navy-700">
            <Link
              href="/"
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                pathname === "/"
                  ? "bg-brand-teal text-white shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-navy-800"
              }`}
            >
              Command Center
            </Link>
            <Link
              href="/evaluation"
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                pathname.startsWith("/evaluation")
                  ? "bg-brand-teal text-white shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-navy-800"
              }`}
            >
              Evaluation & Benchmarks
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden lg:flex items-center gap-2 bg-navy-900 px-3 py-1.5 rounded-lg border border-navy-700 text-xs">
            <span className="text-slate-400">Quick Scenario:</span>
            <select
              className="bg-transparent text-white font-medium focus:outline-none cursor-pointer"
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

          <div
            className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-full border ${
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
    </header>
  );
}
