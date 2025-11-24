type Mode = "diagnostics" | "query";

interface ModeToggleProps {
  mode: Mode;
  onModeChange: (mode: Mode) => void;
}

export function ModeToggle({ mode, onModeChange }: ModeToggleProps) {
  return (
    <div className="mb-8">
      <div className="flex flex-row rounded-lg bg-surface">
        <button
          type="button"
          onClick={() => onModeChange("diagnostics")}
          className={`flex-1 rounded-md py-2 px-2 text-sm font-medium transition-all ${
            mode === "diagnostics"
              ? "bg-accent text-white"
              : "text-muted hover:text-foreground"
          }`}
        >
          Upload & Diagnostics
        </button>
        <button
          type="button"
          onClick={() => onModeChange("query")}
          className={`flex-1 rounded-md py-2 text-sm font-medium transition-all ${
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
