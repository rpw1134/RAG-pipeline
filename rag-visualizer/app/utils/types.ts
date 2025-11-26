/**
 * Distribution bin for histogram data
 */
export interface DistributionBin {
  range: string;
  count: number;
  percentage: number;
}

export interface ChunkBarChartData {
  name: string;
  count: number;
  fill?: string; // Optional color for the bar
}

/**
 * Data for timing pie chart
 */
export interface TimingPieChartData {
  name: string;
  value: number;
  fill: string;
  [key: string]: string | number; // Index signature for Recharts compatibility
}

/**
 * Data for timing stats table
 */
export interface TimingStatsTableData {
  operation: string;
  time: number;
  percentage: number;
}

/**
 * Statistical metrics for a single diagnostic measurement
 */
export interface MetricStatistics {
  mean: number;
  std_dev: number;
  min: number;
  max: number;
  median: number;
  p25: number;
  p75: number;
  pct_in_ideal_range: number;
  distribution: DistributionBin[];
}

/**
 * Chunk diagnostics containing length, cohesion, and separation statistics
 */
export interface ChunkDiagnostics {
  chunk_length: MetricStatistics;
  cohesion: MetricStatistics;
  separation: MetricStatistics;
}

/**
 * Synthetic query evaluation results
 */
export interface SyntheticQueryDiagnostics {
  total_queries: number;
  hits: number;
  misses: number;
  hit_rate: number;
  mrr: number;
  redundancy: number;
}

/**
 * Timing information for pipeline operations
 */
export interface TimingDiagnostics {
  parsing_time: number;
  chunking_time: number;
  embedding_time: number;
  db_insertion_time: number;
}

/**
 * Complete diagnostics object
 */
export interface Diagnostics {
  chunk?: ChunkDiagnostics;
  synthetic?: SyntheticQueryDiagnostics;
  timing: TimingDiagnostics;
}

/**
 * Full API response from the embedding endpoint
 */
export interface EmbeddingResponse {
  diagnostics: Diagnostics;
  num_chunks: number;
}
