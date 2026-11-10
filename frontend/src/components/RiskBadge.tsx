import { RiskLevel } from "@/types";

export default function RiskBadge({ risk }: { risk?: RiskLevel | null }) {
  const tone = risk === "HIGH" ? "bg-red-950/80 text-red-300 border-red-800/80"
    : risk === "MEDIUM" ? "bg-amber-950/80 text-amber-300 border-amber-800/80"
    : risk === "LOW" ? "bg-emerald-950/80 text-emerald-300 border-emerald-800/80"
    : "bg-navy-800 text-slate-300 border-navy-700";
  return <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${tone}`}>
    Assessed risk: {risk ?? "PENDING"}
  </span>;
}
