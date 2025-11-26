import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
  ResponsiveContainer,
} from "recharts";
import { extractChunkGroups } from "@/app/utils/dataTransformation";
import {
  ChunkBarChartData,
  ChunkDiagnostics,
  MetricStatistics,
} from "@/app/utils/types";

interface MetricCardProps {
  title: string;
  data: MetricStatistics;
  idealMin: number;
  idealMax: number;
  unit?: string;
}

function MetricCard({
  title,
  data,
  idealMin,
  idealMax,
  unit = "",
}: MetricCardProps) {
  const distributionData = extractChunkGroups(data, idealMin, idealMax);
  const healthColor =
    data.pct_in_ideal_range >= 80
      ? "text-green-500"
      : data.pct_in_ideal_range >= 50
      ? "text-yellow-500"
      : "text-red-500";

  return (
    <div className="bg-[#282828] rounded-lg p-6 shadow-lg">
      <h3 className="text-xl font-semibold mb-4 text-white">{title}</h3>

      {/* Distribution Chart */}
      <div className="mb-6">
        <p className="text-sm text-gray-400 mb-3">Distribution</p>
        <DistributionBarChart data={distributionData} />
      </div>

      {/* Summary Statistics Grid */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <StatItem label="Mean" value={data.mean.toFixed(1)} unit={unit} />
        <StatItem label="Median" value={data.median.toFixed(1)} unit={unit} />
        <StatItem label="Std Dev" value={data.std_dev.toFixed(2)} unit={unit} />
        <StatItem label="Min" value={data.min.toFixed(1)} unit={unit} />
        <StatItem label="Max" value={data.max.toFixed(1)} unit={unit} />
        <StatItem
          label="P25-P75"
          value={`${data.p25.toFixed(1)}-${data.p75.toFixed(1)}`}
          unit={unit}
        />
      </div>

      {/* Health Indicator */}
      <div className="pt-4 border-t border-gray-700">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-400">In Ideal Range:</span>
          <span className={`text-lg font-bold ${healthColor}`}>
            {data.pct_in_ideal_range.toFixed(1)}%
          </span>
        </div>
        <div className="text-xs text-gray-500 mt-1">
          Ideal: {idealMin}
          {unit} - {idealMax}
          {unit}
        </div>
      </div>
    </div>
  );
}

function StatItem({
  label,
  value,
  unit = "units",
}: {
  label: string;
  value: string;
  unit?: string;
}) {
  return (
    <div className="bg-[#343434] rounded p-3 h-24">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className="text-sm font-semibold text-white">
        {value}
        {unit && <span className="text-gray-500 ml-1">{unit}</span>}
      </p>
    </div>
  );
}

function DistributionBarChart({ data }: { data: ChunkBarChartData[] }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart
        data={data}
        margin={{ top: 5, right: 10, left: -10, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="name" tick={{ fill: "#9ca3af", fontSize: 11 }} />
        <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} width={35} />
        <Tooltip
          contentStyle={{
            backgroundColor: "#d4d4d8",
            border: "1px solid #374151",
            borderRadius: "0.375rem",
            color: "black",
          }}
        />
        <Bar dataKey="count" radius={[4, 4, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.fill || "#22c55e"} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

function ChunkStatsChart({ data }: { data: ChunkDiagnostics | undefined }) {
  if (!data) {
    return (
      <div className="text-white text-center p-8">
        No chunk diagnostics available
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-6">Chunk Diagnostics</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <MetricCard
          title="Chunk Length"
          data={data.chunk_length}
          idealMin={0}
          idealMax={2000}
          unit=" chars"
        />
        <MetricCard
          title="Cohesion Score"
          data={data.cohesion}
          idealMin={0.6}
          idealMax={1.0}
        />
        <MetricCard
          title="Separation Score"
          data={data.separation}
          idealMin={0.1}
          idealMax={0.6}
        />
      </div>
    </div>
  );
}

export { ChunkStatsChart };
