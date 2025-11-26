import { useState } from "react";
import { ChunkStatsChart } from "./charts/ChunkStats";
import SyntheticQueryStatsChart from "./charts/SyntheticQueryStats";
import TimingStatsChart from "./charts/TimingStats";

interface StatsPanelProps {
  mode: "diagnostics" | "query";
}

export function StatsPanel({ mode }: StatsPanelProps) {
  const [tab, setTab] = useState<
    "chunk_stats" | "query_stats" | "timing_stats"
  >("timing_stats");
  return (
    <div className="h-full rounded-lg border border-border bg-surface p-6">
      {tab === "chunk_stats" && <ChunkStatsChart />}
      {tab === "query_stats" && <SyntheticQueryStatsChart />}
      {tab === "timing_stats" && <TimingStatsChart />}
    </div>
  );
}
