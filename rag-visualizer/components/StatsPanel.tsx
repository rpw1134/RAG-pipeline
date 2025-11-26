"use client";

import { useState } from "react";
import { ChunkStatsChart } from "./charts/ChunkStats";
import SyntheticQueryStatsChart from "./charts/SyntheticQueryStats";
import TimingStatsChart from "./charts/TimingStats";
import QueryResults from "./charts/QueryResults";
import { EmbeddingResponse, QueryResponse } from "@/app/utils/types";

interface StatsPanelProps {
  mode: "diagnostics" | "query";
  data: EmbeddingResponse | QueryResponse | null;
}

type TabType = "chunk" | "synthetic" | "timing";

interface Tab {
  id: TabType;
  label: string;
}

const tabs: Tab[] = [
  { id: "timing", label: "Timing" },
  { id: "chunk", label: "Chunk Diagnostics" },
  { id: "synthetic", label: "Retrieval Quality" },
];

// Type guard to check if data is QueryResponse
function isQueryResponse(
  data: EmbeddingResponse | QueryResponse | null
): data is QueryResponse {
  return (
    data !== null &&
    typeof data === "object" &&
    "llm_response" in data &&
    "confidence_score" in data
  );
}

function isDiagnosticsResponse(
  data: EmbeddingResponse | QueryResponse | null
): data is EmbeddingResponse {
  return (
    data !== null &&
    typeof data === "object" &&
    "num_chunks" in data &&
    "diagnostics" in data
  );
}

export function StatsPanel({ mode, data }: StatsPanelProps) {
  const [activeTab, setActiveTab] = useState<TabType>("timing");
  console.log(data);
  if (mode === "query") {
    return (
      <div className="h-full flex flex-col rounded-lg border border-border bg-surface overflow-hidden">
        <div className="flex-1 p-6 overflow-y-auto">
          {!data || !isQueryResponse(data) ? (
            <div className="h-full flex items-center justify-center">
              <div className="bg-[#282828] rounded-lg p-12 max-w-2xl shadow-2xl border border-gray-700">
                <div className="flex items-start gap-6">
                  <div className="text-gray-400 text-8xl">:(</div>
                  <div className="flex-1">
                    <h2 className="text-white text-3xl font-bold mb-4">
                      No Query Results
                    </h2>
                    <p className="text-gray-300 text-lg mb-6">
                      Please submit a query to see results here.
                    </p>
                    <div className="mt-8 text-gray-500 text-xs font-mono">
                      <p>STATUS: WAITING_FOR_QUERY</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <QueryResults data={data} />
          )}
        </div>
      </div>
    );
  }

  if (mode === "diagnostics") {
    return (
      <div className="h-full flex flex-col rounded-lg border border-border bg-surface">
        {!data || !isDiagnosticsResponse(data) ? (
          <div className="h-full flex items-center justify-center">
            <div className="bg-[#282828] rounded-lg p-12 max-w-2xl shadow-2xl border border-gray-700">
              <div className="flex items-start gap-6">
                <div className="text-gray-400 text-8xl">:(</div>
                <div className="flex-1">
                  <h2 className="text-white text-3xl font-bold mb-4">
                    No Diagnostics Data
                  </h2>
                  <p className="text-gray-300 text-lg mb-6">
                    Please upload a document and run diagnostics to see results
                    here.
                  </p>
                  <div className="mt-8 text-gray-500 text-xs font-mono">
                    <p>STATUS: WAITING_FOR_DIAGNOSTICS</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <>
            {/* Tabs Navigation */}
            <div className="shrink-0 bg-[#202020]">
              <div className="flex space-x-1 p-2">
                {tabs.map(
                  (tab) =>
                    data.diagnostics[tab.id] && (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`
                          px-4 py-2.5 rounded-lg font-medium text-lg transition-all cursor-pointer
                          ${
                            activeTab === tab.id
                              ? "text-white shadow-lg"
                              : "text-gray-200 hover:text-white"
                          }
                        `}
                      >
                        {tab.label}
                      </button>
                    )
                )}
              </div>
            </div>

            {/* Tab Content */}
            <div className="flex-1 p-6 overflow-hidden">
              {activeTab === "chunk" && (
                <ChunkStatsChart data={data.diagnostics.chunk} />
              )}
              {activeTab === "synthetic" && (
                <SyntheticQueryStatsChart data={data.diagnostics.synthetic} />
              )}
              {activeTab === "timing" && (
                <TimingStatsChart data={data.diagnostics.timing} />
              )}
            </div>
          </>
        )}
      </div>
    );
  }

  return null;
}
