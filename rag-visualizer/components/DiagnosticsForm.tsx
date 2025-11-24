import { Select, Checkbox, NumberInput } from "@/components/ui";

const EMBEDDING_MODELS = [
  { value: "text-embedding-3-small", label: "text-embedding-3-small" },
  { value: "text-embedding-3-large", label: "text-embedding-3-large" },
  { value: "text-embedding-ada-002", label: "text-embedding-ada-002" },
];

const CHUNKING_STRATEGIES = [
  { value: "recursive", label: "Recursive" },
  { value: "semantic", label: "Semantic" },
  { value: "fixed", label: "Fixed" },
  { value: "sentence", label: "Sentence" },
  { value: "paragraph", label: "Paragraph" },
];

export interface DiagnosticsFormState {
  embeddingModel: string;
  chunkingStrategy: string;
  runChunkDiagnostics: boolean;
  runSyntheticQuery: boolean;
  rerank: boolean;
  rerankReturnNumber: number;
  queryResponseNumber: number;
}

interface DiagnosticsFormProps {
  state: DiagnosticsFormState;
  onChange: (state: DiagnosticsFormState) => void;
}

export function DiagnosticsForm({ state, onChange }: DiagnosticsFormProps) {
  const update = (partial: Partial<DiagnosticsFormState>) => {
    onChange({ ...state, ...partial });
  };

  return (
    <div className="space-y-5">
      <Select
        label="Embedding Model"
        value={state.embeddingModel}
        onChange={(embeddingModel) => update({ embeddingModel })}
        options={EMBEDDING_MODELS}
      />

      <Select
        label="Chunking Strategy"
        value={state.chunkingStrategy}
        onChange={(chunkingStrategy) => update({ chunkingStrategy })}
        options={CHUNKING_STRATEGIES}
      />

      <div className="space-y-3">
        <Checkbox
          label="Run Chunk Diagnostics"
          checked={state.runChunkDiagnostics}
          onChange={(runChunkDiagnostics) => update({ runChunkDiagnostics })}
        />

        <Checkbox
          label="Run Synthetic Query Diagnostics"
          checked={state.runSyntheticQuery}
          onChange={(runSyntheticQuery) => update({ runSyntheticQuery })}
        />
      </div>

      {state.runSyntheticQuery && (
        <div className="space-y-4 rounded-lg border border-border bg-surface p-4">
          <Checkbox
            label="Enable Reranking"
            checked={state.rerank}
            onChange={(rerank) => update({ rerank })}
          />

          {state.rerank && (
            <NumberInput
              label="Rerank Return Number"
              value={state.rerankReturnNumber}
              onChange={(rerankReturnNumber) => update({ rerankReturnNumber })}
            />
          )}

          <NumberInput
            label="Query Response Number"
            value={state.queryResponseNumber}
            onChange={(queryResponseNumber) => update({ queryResponseNumber })}
          />
        </div>
      )}
    </div>
  );
}
