import { ChunkStatsChart } from "./charts/ChunkStats";

interface StatsPanelProps {
  mode: "diagnostics" | "query";
}

export function StatsPanel({ mode }: StatsPanelProps) {
  return (
    <div className="h-full rounded-lg border border-border bg-surface p-6">
      <ChunkStatsChart />
    </div>
  );
}
