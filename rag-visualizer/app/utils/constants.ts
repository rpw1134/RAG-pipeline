import { EmbeddingResponse } from "./types";

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

const EXAMPLE_DIAGNOSTIC_RESPONSE: EmbeddingResponse = {
  diagnostics: {
    chunk: {
      chunk_length: {
        mean: 171.47368421052633,
        std_dev: 223.7546514473416,
        min: 11.0,
        max: 747.0,
        median: 78.0,
        p25: 26.0,
        p75: 196.0,
        pct_in_ideal_range: 100.0,
        distribution: [
          {
            range: "0-500",
            count: 17,
            percentage: 89.47368421052632,
          },
          {
            range: "500-1000",
            count: 2,
            percentage: 10.526315789473683,
          },
          {
            range: "1000-1500",
            count: 0,
            percentage: 0.0,
          },
          {
            range: "1500-2000",
            count: 0,
            percentage: 0.0,
          },
          {
            range: "2000-+",
            count: 0,
            percentage: 0.0,
          },
        ],
      },
      cohesion: {
        mean: 0.6176228523254395,
        std_dev: 0.10561564564704895,
        min: 0.41911137104034424,
        max: 0.8395060300827026,
        median: 0.6225706934928894,
        p25: 0.5736920237541199,
        p75: 0.666662871837616,
        pct_in_ideal_range: 60.0,
        distribution: [
          {
            range: "0.0-0.3",
            count: 0,
            percentage: 0.0,
          },
          {
            range: "0.3-0.5",
            count: 3,
            percentage: 15.0,
          },
          {
            range: "0.5-0.7",
            count: 13,
            percentage: 65.0,
          },
          {
            range: "0.7-0.85",
            count: 4,
            percentage: 20.0,
          },
          {
            range: "0.85-1.0",
            count: 0,
            percentage: 0.0,
          },
        ],
      },
      separation: {
        mean: 0.4778464734554291,
        std_dev: 0.07805921882390976,
        min: 0.312042236328125,
        max: 0.6608197689056396,
        median: 0.46658629179000854,
        p25: 0.4426141381263733,
        p75: 0.502137303352356,
        pct_in_ideal_range: 88.88888888888889,
        distribution: [
          {
            range: "0.0-0.1",
            count: 0,
            percentage: 0.0,
          },
          {
            range: "0.1-0.2",
            count: 0,
            percentage: 0.0,
          },
          {
            range: "0.2-0.4",
            count: 2,
            percentage: 11.11111111111111,
          },
          {
            range: "0.4-0.6",
            count: 14,
            percentage: 77.77777777777779,
          },
          {
            range: "0.6-1.0",
            count: 2,
            percentage: 11.11111111111111,
          },
        ],
      },
    },
    synthetic: {
      total_queries: 16,
      hits: 15,
      misses: 1,
      hit_rate: 0.9375,
      mrr: 0.84375,
      redundancy: 0.3771060034632683,
    },
    timing: {
      parsing_time: 3.645451068878174,
      chunking_time: 7.891654968261719e-5,
      embedding_time: 1.5905630588531494,
      db_insertion_time: 0.020143747329711914,
    },
  },
  num_chunks: 19,
};

export {
  EMBEDDING_MODELS,
  CHUNKING_STRATEGIES,
  LLM_MODELS,
  EXAMPLE_DIAGNOSTIC_RESPONSE,
};
