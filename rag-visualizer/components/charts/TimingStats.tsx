import { EXAMPLE_DIAGNOSTIC_RESPONSE } from "@/app/utils/constants";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import {
  transformTimingForPieChart,
  transformTimingForTable,
  calculateTotalTime,
} from "@/app/utils/dataTransformation";
import { TimingStatsTableData } from "@/app/utils/types";

interface TimingTableProps {
  data: TimingStatsTableData[];
}

function TimingTable({ data }: TimingTableProps) {
  return (
    <div className="overflow-hidden">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-gray-700">
            <th className="py-3 px-4 text-sm font-semibold text-gray-300">
              Operation
            </th>
            <th className="py-3 px-4 text-sm font-semibold text-gray-300 text-right">
              Time (s)
            </th>
            <th className="py-3 px-4 text-sm font-semibold text-gray-300 text-right">
              Percentage
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr
              key={row.operation}
              className={index % 2 === 0 ? "bg-gray-900" : "bg-gray-800"}
            >
              <td className="py-3 px-4 text-sm text-white">{row.operation}</td>
              <td className="py-3 px-4 text-sm text-gray-300 text-right font-mono">
                {row.time.toFixed(4)}
              </td>
              <td className="py-3 px-4 text-sm text-gray-300 text-right">
                {row.percentage.toFixed(1)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function TimingStatsChart() {
  const timing = EXAMPLE_DIAGNOSTIC_RESPONSE.diagnostics.timing;

  if (!timing) {
    return (
      <div className="text-white text-center p-8">
        No timing diagnostics available
      </div>
    );
  }

  const pieData = transformTimingForPieChart(timing);
  const tableData = transformTimingForTable(timing);
  const totalTime = calculateTotalTime(timing);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-6">
        Processing Time Breakdown
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-white text-center">
            Time Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name}: ${((percent || 0) * 100).toFixed(1)}%`
                }
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1f2937",
                  border: "1px solid #374151",
                  borderRadius: "0.375rem",
                  color: "#fff",
                }}
                formatter={(value: number) => `${value.toFixed(4)}s`}
              />
              <Legend
                verticalAlign="bottom"
                height={36}
                iconType="circle"
                wrapperStyle={{ color: "#9ca3af" }}
              />
            </PieChart>
          </ResponsiveContainer>

          {/* Total Time */}
          <div className="mt-6 pt-4 border-t border-gray-700 text-center">
            <p className="text-sm text-gray-400 mb-1">Total Processing Time</p>
            <p className="text-3xl font-bold text-blue-500">
              {totalTime.toFixed(3)}s
            </p>
          </div>
        </div>

        {/* Stats Table */}
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-white">
            Detailed Breakdown
          </h3>
          <TimingTable data={tableData} />

          {/* Performance Insights */}
          <div className="mt-6 pt-4 border-t border-gray-700">
            <p className="text-xs text-gray-400 mb-2">
              <strong className="text-white">Performance Insights:</strong>
            </p>
            <ul className="text-xs text-gray-400 space-y-1 list-disc list-inside">
              <li>
                Parsing typically dominates total time for complex documents
              </li>
              <li>
                Embedding time scales with chunk count and model complexity
              </li>
              <li>Chunking is usually the fastest operation</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
