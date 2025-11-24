"use client";

import { useState } from "react";
import {
  ConfigPanel,
  StatsPanel,
  CollectionStatus,
  type DiagnosticsFormState,
  type QueryFormState,
} from "@/components";

type Mode = "diagnostics" | "query";

const initialDiagnosticsState: DiagnosticsFormState = {
  model: "huggingface_small",
  chunking_strategy: "recursive",
  run_chunk_diagnostics: false,
  run_synthetic_query_diagnostics: false,
  rerank: false,
  num_rerank: 5,
  num_results: 10,
};

const initialQueryState: QueryFormState = {
  query: "",
  embedding_model: "huggingface_small",
  llm_model: "gpt-4o",
  rerank: false,
  num_queries: 10,
  num_results: 5,
  include_metadata: false,
};

export default function Home() {
  const [mode, setMode] = useState<Mode>("diagnostics");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [diagnosticsState, setDiagnosticsState] = useState(
    initialDiagnosticsState
  );
  const [queryState, setQueryState] = useState(initialQueryState);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = mode === "diagnostics" ? diagnosticsState : queryState;
    console.log(formData);
    setIsSubmitted(true);
  };

  return (
    <div className="relative min-h-screen bg-background text-foreground">
      {/* Collection Status - always visible in top right */}
      <CollectionStatus className="fixed top-4 right-4 z-10" />

      {!isSubmitted ? (
        // Centered layout before submission
        <div className="mx-auto max-w-2xl px-6 py-12">
          <ConfigPanel
            mode={mode}
            onModeChange={setMode}
            selectedFile={selectedFile}
            onFileSelect={setSelectedFile}
            diagnosticsState={diagnosticsState}
            onDiagnosticsChange={setDiagnosticsState}
            queryState={queryState}
            onQueryChange={setQueryState}
            onSubmit={handleSubmit}
          />
        </div>
      ) : (
        // Split layout after submission
        <div className="flex min-h-screen">
          {/* Left sidebar - Config panel */}
          <aside className="w-80 shrink-0 border-r border-border bg-surface p-4 overflow-y-auto">
            <ConfigPanel
              compact
              mode={mode}
              onModeChange={setMode}
              selectedFile={selectedFile}
              onFileSelect={setSelectedFile}
              diagnosticsState={diagnosticsState}
              onDiagnosticsChange={setDiagnosticsState}
              queryState={queryState}
              onQueryChange={setQueryState}
              onSubmit={handleSubmit}
            />
          </aside>

          {/* Right content - Stats panel */}
          <main className="flex-1 pl-4 overflow-y-auto">
            <StatsPanel mode={mode} />
          </main>
        </div>
      )}
    </div>
  );
}
