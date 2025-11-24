import { Select, Checkbox, NumberInput } from "@/components/ui";
import { EMBEDDING_MODELS, CHUNKING_STRATEGIES } from "@/app/utils/constants";

export interface DiagnosticsFormState {
  model: string;
  chunking_strategy: string;
  run_chunk_diagnostics: boolean;
  run_synthetic_query_diagnostics: boolean;
  num_results: number;
  num_rerank: number;
  rerank: boolean;
}

interface DiagnosticsFormProps {
  state: DiagnosticsFormState;
  onChange: (state: DiagnosticsFormState) => void;
  compact?: boolean;
}

export function DiagnosticsForm({
  state,
  onChange,
  compact = false,
}: DiagnosticsFormProps) {
  const update = (partial: Partial<DiagnosticsFormState>) => {
    onChange({ ...state, ...partial });
  };

  return (
    <div className={compact ? "space-y-3" : "space-y-5"}>
      <Select
        label="Embedding Model"
        value={state.model}
        onChange={(model) => update({ model })}
        options={EMBEDDING_MODELS}
      />

      <Select
        label="Chunking Strategy"
        value={state.chunking_strategy}
        onChange={(chunking_strategy) => update({ chunking_strategy })}
        options={CHUNKING_STRATEGIES}
      />

      <div className="space-y-3">
        <Checkbox
          label="Run Chunk Diagnostics"
          checked={state.run_chunk_diagnostics}
          onChange={(run_chunk_diagnostics) =>
            update({ run_chunk_diagnostics })
          }
        />

        <Checkbox
          label="Run Synthetic Query Diagnostics"
          checked={state.run_synthetic_query_diagnostics}
          onChange={(run_synthetic_query_diagnostics) =>
            update({ run_synthetic_query_diagnostics })
          }
        />
      </div>

      {state.run_synthetic_query_diagnostics && (
        <div
          className={`rounded-lg border border-border bg-surface ${
            compact ? "space-y-3 p-3" : "space-y-4 p-4"
          }`}
        >
          <Checkbox
            label="Enable Reranking"
            checked={state.rerank}
            onChange={(rerank) => update({ rerank })}
          />

          {state.rerank && (
            <NumberInput
              label="Returned Documents After Rerank"
              value={state.num_rerank}
              onChange={(num_rerank) => update({ num_rerank })}
              max={state.num_results}
            />
          )}

          <NumberInput
            label="Number of Documents to Retrieve"
            value={state.num_results}
            onChange={(num_results) => update({ num_results })}
          />
        </div>
      )}
    </div>
  );
}
