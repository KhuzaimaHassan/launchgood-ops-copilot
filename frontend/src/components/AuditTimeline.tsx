"use client";

import { useState } from "react";
import { AuditEvent } from "@/types";
import { History, ChevronRight, ChevronDown, CheckCircle } from "lucide-react";

interface AuditTimelineProps {
  events: AuditEvent[];
}

export default function AuditTimeline({ events }: AuditTimelineProps) {
  const [showJson, setShowJson] = useState(false);

  const getActorBadge = (actorType: string) => {
    switch (actorType) {
      case "SYSTEM":
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">SYSTEM</span>;
      case "AI_WORKFLOW":
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-brand-teal/20 text-brand-tealLight border border-brand-teal/30">AI WORKFLOW</span>;
      case "REVIEWER":
      case "HUMAN":
      case "HUMAN_REVIEWER":
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">HUMAN REVIEWER</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-navy-800 text-slate-400 border border-navy-700">{actorType}</span>;
    }
  };

  return (
    <div className="bg-navy-900/90 rounded-2xl border border-navy-700 p-6 shadow-xl">
      <div className="flex items-center justify-between pb-4 mb-4 border-b border-navy-800">
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-brand-tealLight" />
          <h3 className="text-sm font-bold text-white">Audit History</h3>
        </div>
        <button
          onClick={() => setShowJson(!showJson)}
          className="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1 bg-navy-800 px-2.5 py-1 rounded-lg border border-navy-700"
        >
          <span>{showJson ? "Hide Raw JSON" : "Inspect Raw JSON"}</span>
          {showJson ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
        </button>
      </div>

      <div className="relative pl-6 border-l-2 border-navy-700 space-y-4 my-2">
        {events.map((evt) => (
          <div key={evt.event_id} className="relative group">
            <div className="absolute -left-[31px] top-1 w-6 h-6 rounded-full bg-navy-900 border-2 border-navy-700 flex items-center justify-center shadow-md">
              <CheckCircle className="w-3.5 h-3.5 text-brand-tealLight" />
            </div>
            <div className="bg-navy-950/60 rounded-xl p-3.5 border border-navy-800">
              <div className="flex items-center justify-between gap-2 mb-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-white">{evt.event_type.replace(/_/g, " ")}</span>
                  {getActorBadge(evt.actor_type)}
                </div>
                <span className="text-[10px] font-mono text-slate-400">{new Date(evt.created_at).toLocaleTimeString()}</span>
              </div>
              <p className="text-[11px] font-mono text-slate-400">Actor: {evt.actor_type}</p>
            </div>
          </div>
        ))}
      </div>

      {showJson && (
        <div className="mt-4 pt-4 border-t border-navy-800">
          <pre className="bg-navy-950 rounded-xl p-4 text-[11px] font-mono text-slate-300 overflow-x-auto max-h-60 border border-navy-800">
            {JSON.stringify(events, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
