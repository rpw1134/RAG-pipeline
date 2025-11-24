"use client";

import { useState } from "react";
import { FileUpload, Button } from "@/components/ui";
import {
  ModeToggle,
  DiagnosticsForm,
  QueryForm,
  type DiagnosticsFormState,
  type QueryFormState,
} from "@/components";

type Mode = "diagnostics" | "query";

const initialDiagnosticsState: DiagnosticsFormState = {
  embeddingModel: "text-embedding-3-small",
  chunkingStrategy: "recursive",
  runChunkDiagnostics: false,
  runSyntheticQuery: false,
  rerank: false,
  rerankReturnNumber: 5,
  queryResponseNumber: 10,
};

const initialQueryState: QueryFormState = {
  query: "",
  embeddingModel: "text-embedding-3-small",
  llmModel: "gpt-4o",
  rerank: false,
  numQueries: 5,
  numResults: 10,
  includeMetadata: false,
};

export default function Home() {
  const [mode, setMode] = useState<Mode>("diagnostics");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [diagnosticsState, setDiagnosticsState] = useState(
    initialDiagnosticsState
  );
  const [queryState, setQueryState] = useState(initialQueryState);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formData =
      mode === "diagnostics"
        ? { mode, file: selectedFile?.name, ...diagnosticsState }
        : { mode, file: selectedFile?.name, ...queryState };
    console.log(formData);
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-2xl px-6 py-12">
        <header className="mb-10 text-center">
          <h1 className="text-3xl font-bold tracking-tight">
            <span className="text-accent">RAG</span> Pipeline
          </h1>
          <p className="mt-2 text-muted">
            Diagnose and query your document pipeline
          </p>
        </header>

        <ModeToggle mode={mode} onModeChange={setMode} />

        <form onSubmit={handleSubmit} className="space-y-6">
          {mode === "diagnostics" && (
            <FileUpload
              selectedFile={selectedFile}
              onFileSelect={setSelectedFile}
            />
          )}

          {mode === "diagnostics" ? (
            <DiagnosticsForm
              state={diagnosticsState}
              onChange={setDiagnosticsState}
            />
          ) : (
            <QueryForm state={queryState} onChange={setQueryState} />
          )}

          <Button type="submit">
            {mode === "diagnostics" ? "Run Diagnostics" : "Submit Query"}
          </Button>
        </form>
      </div>
    </div>
  );
}
