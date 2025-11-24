import { Select, Checkbox, NumberInput, TextArea } from "@/components/ui";

const EMBEDDING_MODELS = [
  { value: "text-embedding-3-small", label: "text-embedding-3-small" },
  { value: "text-embedding-3-large", label: "text-embedding-3-large" },
  { value: "text-embedding-ada-002", label: "text-embedding-ada-002" },
];

const LLM_MODELS = [
  { value: "gpt-4o", label: "gpt-4o" },
  { value: "gpt-4o-mini", label: "gpt-4o-mini" },
  { value: "gpt-4-turbo", label: "gpt-4-turbo" },
  { value: "gpt-3.5-turbo", label: "gpt-3.5-turbo" },
];

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
}

export function QueryForm({ state, onChange }: QueryFormProps) {
  const update = (partial: Partial<QueryFormState>) => {
    onChange({ ...state, ...partial });
  };

  return (
    <div className="space-y-5">
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
          label="Number of Queries"
          value={state.numQueries}
          onChange={(numQueries) => update({ numQueries })}
        />

        {state.rerank && (
          <NumberInput
            label="Number of Results"
            value={state.numResults}
            onChange={(numResults) => update({ numResults })}
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
