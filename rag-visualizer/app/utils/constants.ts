const EMBEDDING_MODELS = [
  { value: "huggingface_small", label: "BAAI/bge-small-en-v1.5" },
  { value: "huggingface_base", label: "BAAI/bge-base-en-v1.5" },
  { value: "huggingface_large", label: "BAAI/bge-large-en-v1.5" },
  { value: "openai_small", label: "OPENAI/text-embedding-3-small" },
  { value: "openai_large", label: "OPENAI/text-embedding-3-large" },
];

const CHUNKING_STRATEGIES = [
  { value: "recursive", label: "Recursive" },
  { value: "structural", label: "Structural" },
  { value: "simple", label: "Fixed" },
];

const LLM_MODELS = [
  { value: "gpt-4o", label: "gpt-4o" },
  { value: "gpt-4o-mini", label: "gpt-4o-mini" },
  { value: "gpt-4-turbo", label: "gpt-4-turbo" },
  { value: "gpt-3.5-turbo", label: "gpt-3.5-turbo" },
];

export { EMBEDDING_MODELS, CHUNKING_STRATEGIES, LLM_MODELS };
