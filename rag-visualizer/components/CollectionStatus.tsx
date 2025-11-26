"use client";

import { useEffect, useState } from "react";
import { EMBEDDING_MODELS } from "@/app/utils/constants";

interface CollectionStatusProps {
  className?: string;
  refreshTrigger?: number;
}

export function CollectionStatus({
  className = "",
  refreshTrigger = 0,
}: CollectionStatusProps) {
  const [activeCollections, setActiveCollections] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [clearing, setClearing] = useState<string | null>(null);
  const [isCollapsed, setIsCollapsed] = useState(false);

  const fetchCollections = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/collections?active_only=true"
      );
      if (response.ok) {
        const data = await response.json();
        setActiveCollections(data.collections);
      }
    } catch (error) {
      console.error("Failed to fetch collections:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCollections();
  }, [refreshTrigger]);

  const isActive = (modelValue: string) => {
    return activeCollections.includes(modelValue);
  };

  const handleClear = async (collectionName: string) => {
    setClearing(collectionName);
    try {
      const response = await fetch(
        `http://localhost:8000/collections/${collectionName}`,
        { method: "DELETE" }
      );
      if (response.ok) {
        await fetchCollections();
      }
    } catch (error) {
      console.error("Failed to clear collection:", error);
    } finally {
      setClearing(null);
    }
  };

  return (
    <div
      className={`rounded-lg border border-border bg-surface p-3 ${className}`}
    >
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="w-full flex items-center justify-between mb-2 hover:opacity-80 transition-opacity"
      >
        <h3 className="text-xs font-semibold text-muted uppercase tracking-wide">
          Collections
        </h3>
        <svg
          className={`w-4 h-4 text-muted transition-transform duration-200 ${
            isCollapsed ? "-rotate-90" : ""
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      <div
        className={`overflow-hidden transition-all duration-200 ${
          isCollapsed ? "max-h-0 opacity-0" : "max-h-96 opacity-100"
        }`}
      >
        <div className="space-y-1.5">
          {EMBEDDING_MODELS.map((model) => {
            const active = isActive(model.value);
            const isClearing = clearing === model.value;

            return (
              <div key={model.value} className="flex items-center gap-2">
                <span
                  className={`h-2 w-2 shrink-0 rounded-full ${
                    loading || isClearing
                      ? "bg-muted animate-pulse"
                      : active
                      ? "bg-green-500"
                      : "bg-red-500"
                  }`}
                  title={
                    loading || isClearing
                      ? "Fetching Collection"
                      : active
                      ? "Populated"
                      : "Empty"
                  }
                />
                <span className="flex-1 text-xs text-foreground truncate">
                  {model.label.split("/")[1] || model.label}
                </span>
                {active && !loading && (
                  <button
                    type="button"
                    onClick={() => handleClear(model.value)}
                    disabled={isClearing}
                    className="text-xs text-muted hover:text-red-400 transition-colors disabled:opacity-50 cursor-pointer"
                    title={`Clear ${model.value}`}
                  >
                    {isClearing ? "..." : "×"}
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
