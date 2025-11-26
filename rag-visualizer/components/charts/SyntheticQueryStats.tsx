import {
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
  ResponsiveContainer,
} from "recharts";
import { SyntheticQueryDiagnostics } from "@/app/utils/types";

interface GaugeCardProps {
  title: string;
  value: number;
  color: string;
  subtitle?: string;
}

function GaugeCard({ title, value, color, subtitle }: GaugeCardProps) {
  const data = [{ name: title, value: value * 100, fill: color }];

  const getColorClass = () => {
    if (value >= 0.8) return "text-green-500";
    if (value >= 0.6) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <div className="bg-[#282828] rounded-lg p-6 shadow-lg h-96">
      <h3 className="text-lg font-semibold mb-2 text-white text-center">
        {title}
      </h3>
      {subtitle && (
        <p className="text-xs text-gray-400 text-center mb-4">{subtitle}</p>
      )}

      <div className="relative flex items-center justify-center h-96">
        <ResponsiveContainer width={300} height={300}>
          <RadialBarChart
            innerRadius="70%"
            outerRadius="100%"
            data={data}
            startAngle={180}
            endAngle={0}
          >
            <PolarAngleAxis
              type="number"
              domain={[0, 100]}
              angleAxisId={0}
              tick={false}
            />
            <RadialBar
              background
              dataKey="value"
              cornerRadius={10}
              fill={color}
            />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex items-center justify-center pt-12">
          <p className={`text-4xl font-bold ${getColorClass()}`}>
            {(value * 100).toFixed(1)}%
          </p>
        </div>
      </div>
    </div>
  );
}

interface MetricBoxProps {
  label: string;
  value: string | number;
  subtext?: string;
  colorClass?: string;
}

function MetricBox({
  label,
  value,
  subtext,
  colorClass = "text-blue-500",
}: MetricBoxProps) {
  return (
    <div className="bg-[#282828] rounded-lg p-6 shadow-lg">
      <p className="text-sm text-gray-400 mb-2">{label}</p>
      <p className={`text-3xl font-bold ${colorClass}`}>{value}</p>
      {subtext && <p className="text-xs text-gray-500 mt-2">{subtext}</p>}
    </div>
  );
}

export default function SyntheticQueryStatsChart({
  data,
}: {
  data: SyntheticQueryDiagnostics | undefined;
}) {
  if (!data) {
    return (
      <div className="text-white text-center p-8">
        No synthetic query diagnostics available
      </div>
    );
  }

  const getRedundancyColor = () => {
    if (data.redundancy < 0.5) return "text-green-500";
    if (data.redundancy < 0.7) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-6">
        Retrieval Quality Diagnostics
      </h2>

      {/* Gauges for Hit Rate and MRR */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <GaugeCard
          title="Hit Rate"
          value={data.hit_rate}
          color="#22c55e"
          subtitle="% of queries that retrieved the expected document"
        />
        <GaugeCard
          title="Mean Reciprocal Rank"
          value={data.mrr}
          color="#3b82f6"
          subtitle="Average ranking position of expected documents"
        />
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricBox
          label="Total Queries"
          value={data.total_queries}
          colorClass="text-gray-300"
        />
        <MetricBox
          label="Hits / Misses"
          value={`${data.hits} / ${data.misses}`}
          colorClass="text-green-500"
          subtext={`${((data.hits / data.total_queries) * 100).toFixed(
            1
          )}% success rate`}
        />
        <MetricBox
          label="Redundancy Score"
          value={`${(data.redundancy * 100).toFixed(1)}%`}
          colorClass={getRedundancyColor()}
          subtext="Lower is better (more diverse results)"
        />
      </div>

      {/* Explanation */}
      <div className="bg-[#282828] rounded-lg p-4 mt-6">
        <p className="text-xs text-gray-400">
          <strong className="text-white">Note:</strong> These metrics evaluate
          how well the retrieval system finds expected documents. Hit Rate shows
          the percentage of successful retrievals, MRR indicates how highly the
          expected documents are ranked, and Redundancy measures result
          diversity.
        </p>
      </div>
    </div>
  );
}
