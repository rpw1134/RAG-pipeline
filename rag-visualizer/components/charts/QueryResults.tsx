import { QueryResponse } from "@/app/utils/types";

interface QueryResultsProps {
  data: QueryResponse;
}

export default function QueryResults({ data }: QueryResultsProps) {
  if (!data || !data.llm_response) {
    return (
      <div className="text-white text-center p-8">
        No query results available
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Top Section: LLM Response and Confidence Score */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LLM Response */}
        <div className="bg-[#282828] rounded-lg p-8 shadow-lg">
          <h3 className="text-2xl font-semibold mb-4 text-white underline underline-offset-8">
            LLM Response
          </h3>
          <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
            {data.llm_response}
          </div>
        </div>

        {/* Confidence Score */}
        <div className="bg-[#282828] rounded-lg p-8 shadow-lg flex flex-col items-center justify-center">
          <h3 className="text-2xl font-semibold mb-6 text-white">
            Confidence Score
          </h3>
          <div className="text-8xl font-bold text-green-500">
            {(data.confidence_score ?? 0).toFixed(1)}%
          </div>
          <p className="text-gray-400 mt-4 text-sm">
            Model confidence in the generated response
          </p>
        </div>
      </div>

      {/* Bottom Section: Retrieved Context */}
      <div className="bg-[#282828] rounded-lg p-8 shadow-lg">
        <h3 className="text-2xl font-semibold mb-6 text-white">
          Retrieved Context
        </h3>
        <div className="space-y-4">
          {data.context_returned?.map((context, index) => {
            const [text] = context;
            const score = data.context_scores?.[index] ?? 0;

            return (
              <div
                key={index}
                className="bg-[#323232] rounded-lg p-6 border border-gray-700"
              >
                <div className="flex items-start justify-between gap-6">
                  {/* Document Text */}
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-sm font-semibold text-gray-400">
                        Document {index + 1}
                      </span>
                    </div>
                    <p className="text-gray-300 text-base whitespace-pre-wrap">
                      {text}
                    </p>
                  </div>

                  {/* Context Score */}
                  <div className="shrink-0 text-right">
                    <p className="text-sm text-gray-400 mb-1">Score</p>
                    <p className="text-2xl font-bold text-gray-300">
                      {score.toFixed(2)}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
