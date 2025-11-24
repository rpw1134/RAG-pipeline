interface StatsPanelProps {
  mode: "diagnostics" | "query";
}

export function StatsPanel({ mode }: StatsPanelProps) {
  return (
    <div className="h-full rounded-lg border border-border bg-surface p-6">
      <h2 className="mb-4 text-xl font-semibold">
        {mode === "diagnostics" ? "Diagnostics Results" : "Query Results"}
      </h2>
      <div className="flex h-64 items-center justify-center text-muted">
        <p>Results will appear here...</p>
      </div>
    </div>
  );
}
