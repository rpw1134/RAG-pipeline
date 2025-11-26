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
import { TimingStatsTableData, TimingDiagnostics } from "@/app/utils/types";

interface TimingTableProps {
  data: TimingStatsTableData[];
}

function TimingTable({ data }: TimingTableProps) {
  return (
    <div className="overflow-hidden">
      <table className="w-full text-left h-76">
        <thead>
          <tr className="">
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
              className={index % 2 === 0 ? "bg-[#323232]" : "bg-[#3f3f3f]"}
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

export default function TimingStatsChart({
  data,
}: {
  data: TimingDiagnostics | undefined;
}) {
  if (!data) {
    return (
      <div className="text-white text-center p-8">
        No timing diagnostics available
      </div>
    );
  }

  const pieData = transformTimingForPieChart(data);
  const tableData = transformTimingForTable(data);
  const totalTime = calculateTotalTime(data);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white mb-6">
        Processing Time Breakdown
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="bg-[#282828] rounded-lg p-6 shadow-lg lg:h-[36rem]">
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
                label={({ name, percent, x, y }) => (
                  <text
                    x={x}
                    y={y}
                    fill="#d1d5db"
                    fontSize="14px"
                    textAnchor={x > 200 ? "start" : "end"}
                  >
                    {`${name}: ${((percent || 0) * 100).toFixed(1)}%`}
                  </text>
                )}
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
                  backgroundColor: "#d4d4d8",
                  border: "1px solid #374151",
                  borderRadius: "0.375rem",
                  color: "black",
                }}
                formatter={(value: number) => `${value.toFixed(4)}s`}
              />
              <Legend
                verticalAlign="bottom"
                height={60}
                iconType="circle"
                wrapperStyle={{ color: "#d1d5db", paddingTop: "20px" }}
              />
            </PieChart>
          </ResponsiveContainer>

          {/* Total Time */}
          <div className="mt-6 pt-4 border-t border-black text-center">
            <p className="text-sm text-gray-400 mb-1">Total Processing Time</p>
            <p className="text-3xl font-bold text-gray-300">
              {totalTime.toFixed(3)}s
            </p>
          </div>
        </div>

        {/* Stats Table */}
        <div className="bg-[#282828] rounded-lg p-6 shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-white">
            Detailed Breakdown
          </h3>
          <TimingTable data={tableData} />

          {/* Performance Insights */}
          <div className="mt-6 pt-4 border-t border-black">
            <p className="text-sm text-gray-400 mb-2">
              <strong className="text-white">Performance Insights:</strong>
            </p>
            <ul className="text-sm text-gray-400 space-y-1 list-disc list-inside">
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
