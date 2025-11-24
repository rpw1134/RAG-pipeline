import { Select, Checkbox, NumberInput, TextArea } from "@/components/ui";
import { EMBEDDING_MODELS, LLM_MODELS } from "@/app/utils/constants";

export interface QueryFormState {
  query: string;
  embeddingModel: string;
  llmModel: string;
  rerank: boolean;
  numQueries: number;
  numResults: number;
  includeMetadata: boolean;
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
        value={state.embeddingModel}
        onChange={(embeddingModel) => update({ embeddingModel })}
        options={EMBEDDING_MODELS}
      />

      <Select
        label="LLM Model"
        value={state.llmModel}
        onChange={(llmModel) => update({ llmModel })}
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
          value={state.numQueries}
          onChange={(numQueries) => update({ numQueries })}
        />

        {state.rerank && (
          <NumberInput
            label="Returned Documents After Rerank"
            value={state.numResults}
            onChange={(numResults) => update({ numResults })}
            max={state.numQueries}
          />
        )}
      </div>

      <Checkbox
        label="Include Metadata"
        checked={state.includeMetadata}
        onChange={(includeMetadata) => update({ includeMetadata })}
      />
    </div>
  );
}
