type Mode = "diagnostics" | "query";

interface ModeToggleProps {
  mode: Mode;
  onModeChange: (mode: Mode) => void;
}

export function ModeToggle({ mode, onModeChange }: ModeToggleProps) {
  return (
    <div className="mb-8 flex justify-center">
      <div className="inline-flex rounded-lg bg-surface p-1">
        <button
          type="button"
          onClick={() => onModeChange("diagnostics")}
          className={`rounded-md px-6 py-2 text-sm font-medium transition-all ${
            mode === "diagnostics"
              ? "bg-accent text-white"
              : "text-muted hover:text-foreground"
          }`}
        >
          Diagnostics
        </button>
        <button
          type="button"
          onClick={() => onModeChange("query")}
          className={`rounded-md px-6 py-2 text-sm font-medium transition-all ${
            mode === "query"
              ? "bg-accent text-white"
              : "text-muted hover:text-foreground"
          }`}
        >
          Query
        </button>
      </div>
    </div>
  );
}
