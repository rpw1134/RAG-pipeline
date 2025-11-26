import {
  ChunkBarChartData,
  MetricStatistics,
  TimingDiagnostics,
  TimingPieChartData,
  TimingStatsTableData,
} from "./types";

/**
 * Extract distribution data for bar charts with optional color coding
 */
export function extractChunkGroups(
  metricData: MetricStatistics,
  idealMin?: number,
  idealMax?: number
): ChunkBarChartData[] {
  const groups: ChunkBarChartData[] = [];
  for (const dist of metricData.distribution) {
    const color = getColorForRange(
      dist.range,
      idealMin,
      idealMax,
      dist.percentage
    );
    groups.push({ name: dist.range, count: dist.count, fill: color });
  }
  return groups;
}

/**
 * Get color for a distribution bin based on ideal range
 */
function getColorForRange(
  range: string,
  idealMin?: number,
  idealMax?: number,
  percentage?: number
): string {
  if (!idealMin || !idealMax) {
    return "#f97316"; // Default orange
  }

  // Parse the range string (e.g., "500-1000" or "2000-+")
  const [minStr, maxStr] = range.split("-");
  const min = parseFloat(minStr);
  const max = maxStr === "+" ? Infinity : parseFloat(maxStr);

  // Check if this bin is in the ideal range
  const isInIdealRange =
    (min >= idealMin && min < idealMax) || (max > idealMin && max <= idealMax);

  // Green for ideal, yellow for adjacent, red for far
  if (isInIdealRange) {
    return "#22c55e"; // Green
  } else if (
    (max === idealMin || min === idealMax) &&
    percentage &&
    percentage > 10
  ) {
    return "#eab308"; // Yellow for adjacent bins with significant data
  } else {
    return "#ef4444"; // Red
  }
}

/**
 * Transform timing data for pie chart
 */
export function transformTimingForPieChart(
  timing: TimingDiagnostics
): TimingPieChartData[] {
  const colors = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b"];

  return [
    {
      name: "Parsing",
      value: parseFloat(timing.parsing_time.toFixed(3)),
      fill: colors[0],
    },
    {
      name: "Chunking",
      value: parseFloat(timing.chunking_time.toFixed(3)),
      fill: colors[1],
    },
    {
      name: "Embedding",
      value: parseFloat(timing.embedding_time.toFixed(3)),
      fill: colors[2],
    },
    {
      name: "DB Insert",
      value: parseFloat(timing.db_insertion_time.toFixed(3)),
      fill: colors[3],
    },
  ];
}

/**
 * Transform timing data for stats table
 */
export function transformTimingForTable(
  timing: TimingDiagnostics
): TimingStatsTableData[] {
  const total =
    timing.parsing_time +
    timing.chunking_time +
    timing.embedding_time +
    timing.db_insertion_time;

  return [
    {
      operation: "Parsing",
      time: timing.parsing_time,
      percentage: (timing.parsing_time / total) * 100,
    },
    {
      operation: "Chunking",
      time: timing.chunking_time,
      percentage: (timing.chunking_time / total) * 100,
    },
    {
      operation: "Embedding",
      time: timing.embedding_time,
      percentage: (timing.embedding_time / total) * 100,
    },
    {
      operation: "DB Insert",
      time: timing.db_insertion_time,
      percentage: (timing.db_insertion_time / total) * 100,
    },
  ];
}

/**
 * Calculate total time from timing diagnostics
 */
export function calculateTotalTime(timing: TimingDiagnostics): number {
  return (
    timing.parsing_time +
    timing.chunking_time +
    timing.embedding_time +
    timing.db_insertion_time
  );
}
