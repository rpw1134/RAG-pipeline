"use client";

import { FileUpload, Button } from "@/components/ui";
import {
  ModeToggle,
  DiagnosticsForm,
  QueryForm,
  type DiagnosticsFormState,
  type QueryFormState,
} from "@/components";

type Mode = "diagnostics" | "query";

interface ConfigPanelProps {
  compact?: boolean;
  mode: Mode;
  onModeChange: (mode: Mode) => void;
  selectedFile: File | null;
  onFileSelect: (file: File) => void;
  diagnosticsState: DiagnosticsFormState;
  onDiagnosticsChange: (state: DiagnosticsFormState) => void;
  queryState: QueryFormState;
  onQueryChange: (state: QueryFormState) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function ConfigPanel({
  compact = false,
  mode,
  onModeChange,
  selectedFile,
  onFileSelect,
  diagnosticsState,
  onDiagnosticsChange,
  queryState,
  onQueryChange,
  onSubmit,
}: ConfigPanelProps) {
  return (
    <div className={compact ? "mt-4 space-y-4" : "space-y-6"}>
      {!compact && (
        <header className="mb-10 text-center">
          <h1 className="text-3xl font-bold tracking-tight">
            <span className="text-accent">RAG</span> Pipeline Visualizer
          </h1>
          <p className="mt-2 text-muted">
            Find what strategies, models, and methods work best for your data.
          </p>
        </header>
      )}

      <ModeToggle mode={mode} onModeChange={onModeChange} />

      <form onSubmit={onSubmit} className={compact ? "space-y-4" : "space-y-6"}>
        {mode === "diagnostics" && (
          <FileUpload
            selectedFile={selectedFile}
            onFileSelect={onFileSelect}
            compact={compact}
          />
        )}

        {mode === "diagnostics" ? (
          <DiagnosticsForm
            state={diagnosticsState}
            onChange={onDiagnosticsChange}
            compact={compact}
          />
        ) : (
          <QueryForm
            state={queryState}
            onChange={onQueryChange}
            compact={compact}
          />
        )}

        <Button type="submit">
          {mode === "diagnostics"
            ? compact
              ? "Re-run"
              : "Upload Context & Run Diagnostics"
            : "Submit Query"}
        </Button>
      </form>
    </div>
  );
}
