import { Select, Checkbox, NumberInput, TextArea } from "@/components/ui";
import { EMBEDDING_MODELS, LLM_MODELS } from "@/app/utils/constants";

export interface QueryFormState {
  query: string;
  embedding_model: string;
  llm_model: string;
  rerank: boolean;
  num_queries: number;
  num_results: number;
  include_metadata: boolean;
}

interface QueryFormProps {
  state: QueryFormState;
  onChange: (state: QueryFormState) => void;
  compact?: boolean;
}

export function QueryForm({
  state,
  onChange,
  compact = false,
}: QueryFormProps) {
  const update = (partial: Partial<QueryFormState>) => {
    onChange({ ...state, ...partial });
  };

  return (
    <div className={compact ? "space-y-3" : "space-y-5"}>
      <TextArea
        label="Query"
        value={state.query}
        onChange={(query) => update({ query })}
        placeholder="Enter your query..."
      />

      <Select
        label="Embedding Model"
        value={state.embedding_model}
        onChange={(embedding_model) => update({ embedding_model })}
        options={EMBEDDING_MODELS}
      />

      <Select
        label="LLM Model"
        value={state.llm_model}
        onChange={(llm_model) => update({ llm_model })}
        options={LLM_MODELS}
      />

      <Checkbox
        label="Enable Reranking"
        checked={state.rerank}
        onChange={(rerank) => update({ rerank })}
      />

      <div className="grid grid-cols-2 gap-4">
        <NumberInput
          label="Documents to Retrieve from Database"
          value={state.num_queries}
          onChange={(num_queries) => update({ num_queries })}
        />

        {state.rerank && (
          <NumberInput
            label="Returned Documents After Rerank"
            value={state.num_results}
            onChange={(num_results) => update({ num_results })}
            max={state.num_queries}
          />
        )}
      </div>

      <Checkbox
        label="Include Metadata"
        checked={state.include_metadata}
        onChange={(include_metadata) => update({ include_metadata })}
      />
    </div>
  );
}
