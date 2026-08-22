import { ReactNode } from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  note: string;
  icon?: ReactNode;
  tone?: "teal" | "red" | "amber" | "green" | "slate";
}

export default function MetricCard({ label, value, note, icon, tone = "teal" }: MetricCardProps) {
  const borderColors = {
    teal: "border-brand-teal/40 hover:border-brand-teal",
    red: "border-red-500/40 hover:border-red-500",
    amber: "border-amber-500/40 hover:border-amber-500",
    green: "border-emerald-500/40 hover:border-emerald-500",
    slate: "border-navy-600 hover:border-slate-500",
  };

  const noteColors = {
    teal: "text-brand-tealLight",
    red: "text-red-400",
    amber: "text-amber-400",
    green: "text-emerald-400",
    slate: "text-slate-400",
  };

  return (
    <div
      className={`bg-navy-900/90 rounded-2xl p-5 border ${borderColors[tone]} transition-all duration-200 shadow-lg shadow-navy-950/40 flex flex-col justify-between`}
    >
      <div className="flex items-center justify-between">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{label}</span>
        {icon && <div className="text-slate-400">{icon}</div>}
      </div>
      <div className="my-2">
        <span className="text-3xl font-extrabold tracking-tight text-white">{value}</span>
      </div>
      <div className={`text-xs font-medium ${noteColors[tone]}`}>{note}</div>
    </div>
  );
}
