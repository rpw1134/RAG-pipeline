"use client";

import { useState } from "react";
import {
  ConfigPanel,
  StatsPanel,
  CollectionStatus,
  type DiagnosticsFormState,
  type QueryFormState,
} from "@/components";
import { EmbeddingResponse, QueryResponse } from "./utils/types";

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
  const [isPondering, setIsPondering] = useState(false);
  const [collectionRefresh, setCollectionRefresh] = useState(0);
  const [responseData, setResponseData] = useState<
    EmbeddingResponse | QueryResponse | null
  >(null);
  const [diagnosticsData, setDiagnosticsData] =
    useState<EmbeddingResponse | null>(null);
  const [queryData, setQueryData] = useState<QueryResponse | null>(null);

  const handleConfigSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsPondering(true);

    try {
      let response;
      const formData = new FormData();
      const config = mode === "diagnostics" ? diagnosticsState : queryState;

      if (mode === "diagnostics") {
        const file = mode === "diagnostics" ? selectedFile : null;
        if (file) {
          formData.append("file", file);
        }
        formData.append("config", JSON.stringify(config));
        console.log("Submitting config:", config);
        console.log("Submitting file:", file);
        response = await fetch("http://localhost:8000/embeddings/documents", {
          method: "POST",
          body: formData,
        });
        const data: EmbeddingResponse = await response.json();
        setResponseData(data);
        setDiagnosticsData(data);
        setMode("diagnostics");
      } else {
        // Validate query is not empty
        if (!queryState.query || queryState.query.trim() === "") {
          alert("Please enter a query");
          setIsPondering(false);
          return;
        }

        // Send JSON for query mode — stringify the config and set Content-Type header
        console.log("Submitting query config:", config);
        response = await fetch("http://localhost:8000/queries", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(config),
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error("Query submission error:", errorText);
          alert(`Error: ${errorText}`);
          setIsPondering(false);
          return;
        }

        const data: QueryResponse = await response.json();
        console.log("Query response:", data);
        setResponseData(data);
        setQueryData(data);
        setMode("query");
      }
      setCollectionRefresh((prev) => prev + 1);
      setIsSubmitted(true);
    } catch (error) {
      console.error("Error submitting:", error);
      alert(`Error: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsPondering(false);
    }
  };

  const handleChangeMode = (newMode: Mode) => {
    console.log("diagnostic:", diagnosticsData);
    console.log("query", queryData);
    setResponseData(newMode === "diagnostics" ? diagnosticsData : queryData);
    setMode(newMode);
  };

  return (
    <div className="relative min-h-screen bg-background text-foreground">
      {/* Collection Status - always visible in top right */}
      <CollectionStatus
        className="fixed top-4 right-4 z-10"
        refreshTrigger={collectionRefresh}
      />

      {!isSubmitted ? (
        // Centered layout before submission
        <div className="mx-auto max-w-2xl px-6 py-12">
          <ConfigPanel
            mode={mode}
            onModeChange={handleChangeMode}
            selectedFile={selectedFile}
            onFileSelect={setSelectedFile}
            diagnosticsState={diagnosticsState}
            onDiagnosticsChange={setDiagnosticsState}
            queryState={queryState}
            onQueryChange={setQueryState}
            onSubmit={handleConfigSubmit}
            isPondering={isPondering}
          />
        </div>
      ) : (
        // Split layout after submission
        <div className="flex h-screen">
          {/* Left sidebar - Config panel */}
          <aside className="w-80 shrink-0 border-r border-border bg-surface p-4 overflow-y-auto">
            <ConfigPanel
              compact
              mode={mode}
              onModeChange={handleChangeMode}
              selectedFile={selectedFile}
              onFileSelect={setSelectedFile}
              diagnosticsState={diagnosticsState}
              onDiagnosticsChange={setDiagnosticsState}
              queryState={queryState}
              onQueryChange={setQueryState}
              onSubmit={handleConfigSubmit}
              isPondering={isPondering}
            />
          </aside>

          {/* Right content - Stats panel */}
          <main className="flex-1 p-4 overflow-hidden">
            <StatsPanel mode={mode} data={responseData} />
          </main>
        </div>
      )}
    </div>
  );
}
