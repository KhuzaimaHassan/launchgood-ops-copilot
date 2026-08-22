import { Case } from "@/types";
import { MessageSquare, Bell, AlertTriangle, FileText, CheckCircle2 } from "lucide-react";

interface SourceTimelineProps {
  caseData: Case;
}

export default function SourceTimeline({ caseData }: SourceTimelineProps) {
  const events: Array<{
    id: string;
    type: "CAMPAIGN" | "MESSAGE" | "UPDATE" | "SIGNAL";
    title: string;
    subtitle?: string | null;
    content: string;
    timestamp: string;
    sourceId: string;
  }> = [
    {
      id: "camp-init",
      type: "CAMPAIGN",
      title: "Campaign Created",
      subtitle: caseData.campaign.organizer_summary,
      content: caseData.campaign.description,
      timestamp: caseData.campaign.created_at,
      sourceId: caseData.campaign.campaign_id,
    },
    ...caseData.support_messages.map((m) => ({
      id: m.source_id,
      type: "MESSAGE" as const,
      title: `Support Inquiry (${m.author_role})`,
      subtitle: `Channel: ${m.channel}`,
      content: m.content,
      timestamp: m.created_at,
      sourceId: m.source_id,
    })),
    ...caseData.campaign_updates.map((u) => ({
      id: u.source_id,
      type: "UPDATE" as const,
      title: "Organizer Campaign Update",
      subtitle: "Public Post",
      content: u.content,
      timestamp: u.created_at,
      sourceId: u.source_id,
    })),
    ...caseData.risk_signals.map((s) => ({
      id: s.signal_id,
      type: "SIGNAL" as const,
      title: `Automated Risk Signal (${s.severity})`,
      subtitle: s.signal_type,
      content: typeof s.value === "string" ? s.value : JSON.stringify(s.value),
      timestamp: s.created_at || caseData.created_at,
      sourceId: s.signal_id,
    })),
  ];

  events.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  const getIcon = (type: string) => {
    switch (type) {
      case "CAMPAIGN":
        return <FileText className="w-4 h-4 text-brand-tealLight" />;
      case "MESSAGE":
        return <MessageSquare className="w-4 h-4 text-blue-400" />;
      case "UPDATE":
        return <Bell className="w-4 h-4 text-amber-400" />;
      case "SIGNAL":
        return <AlertTriangle className="w-4 h-4 text-red-400" />;
      default:
        return <CheckCircle2 className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="space-y-4">
      <div className="relative pl-6 border-l-2 border-navy-700 space-y-6 my-2">
        {events.map((evt) => (
          <div key={evt.id} className="relative group">
            <div className="absolute -left-[31px] top-1 w-6 h-6 rounded-full bg-navy-900 border-2 border-navy-700 flex items-center justify-center shadow-md">
              {getIcon(evt.type)}
            </div>
            <div className="bg-navy-900/80 rounded-xl p-4 border border-navy-700/80 hover:border-navy-600 transition-colors shadow-sm">
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-white">{evt.title}</span>
                  <span className="font-mono text-[10px] text-slate-400 bg-navy-950 px-1.5 py-0.5 rounded border border-navy-800">
                    {evt.sourceId}
                  </span>
                </div>
                <span className="text-[10px] font-mono text-slate-400">{new Date(evt.timestamp).toLocaleString()}</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{evt.content}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
