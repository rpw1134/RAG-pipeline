"use client";

import { useEffect, useState } from "react";
import { EMBEDDING_MODELS } from "@/app/utils/constants";

interface CollectionStatusProps {
  className?: string;
}

export function CollectionStatus({ className = "" }: CollectionStatusProps) {
  const [activeCollections, setActiveCollections] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/collections?active_only=true"
        );
        if (response.ok) {
          const data = await response.json();
          console.log("Fetched collections:", data);
          setActiveCollections(data.collections);
        }
      } catch (error) {
        console.error("Failed to fetch collections:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCollections();
  }, []);

  const isActive = (modelValue: string) => {
    console.log(activeCollections);
    return activeCollections.includes(modelValue);
  };

  return (
    <div
      className={`rounded-lg border border-border bg-surface p-3 ${className}`}
    >
      <h3 className="mb-2 text-xs font-semibold text-muted uppercase tracking-wide">
        Collections
      </h3>
      <div className="space-y-1.5">
        {EMBEDDING_MODELS.map((model) => (
          <div key={model.value} className="flex items-center gap-2">
            <span
              className={`h-2 w-2 rounded-full ${
                loading
                  ? "bg-muted animate-pulse"
                  : isActive(model.value)
                  ? "bg-green-500"
                  : "bg-red-500"
              }`}
            />
            <span className="text-xs text-foreground truncate">
              {model.label.split("/")[1] || model.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
