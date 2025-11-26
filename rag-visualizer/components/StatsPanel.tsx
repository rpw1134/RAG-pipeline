"use client";

import { useState } from "react";
import { ChunkStatsChart } from "./charts/ChunkStats";
import SyntheticQueryStatsChart from "./charts/SyntheticQueryStats";
import TimingStatsChart from "./charts/TimingStats";
import { EmbeddingResponse } from "@/app/utils/types";

interface StatsPanelProps {
  mode: "diagnostics" | "query";
  data: EmbeddingResponse | null;
}

type TabType = "chunk" | "synthetic" | "timing";

interface Tab {
  id: TabType;
  label: string;
}

const tabs: Tab[] = [
  { id: "chunk", label: "Chunk Diagnostics" },
  { id: "synthetic", label: "Retrieval Quality" },
  { id: "timing", label: "Timing" },
];

export function StatsPanel({ mode, data }: StatsPanelProps) {
  const [activeTab, setActiveTab] = useState<TabType>("chunk");

  if (mode === "diagnostics") {
    return (
      <div className="h-full flex flex-col rounded-lg border border-border bg-surface">
        {/* Tabs Navigation */}
        <div className="shrink-0 bg-[#202020]">
          <div className="flex space-x-1 p-2">
            {tabs.map(
              (tab) =>
                data &&
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
          {!data ? (
            <div className="text-white text-center p-8">
              No diagnostics data available
            </div>
          ) : (
            <>
              {activeTab === "chunk" && (
                <ChunkStatsChart data={data!.diagnostics.chunk} />
              )}
              {activeTab === "synthetic" && (
                <SyntheticQueryStatsChart data={data!.diagnostics.synthetic} />
              )}
              {activeTab === "timing" && (
                <TimingStatsChart data={data!.diagnostics.timing} />
              )}
            </>
          )}
        </div>
      </div>
    );
  }
}
