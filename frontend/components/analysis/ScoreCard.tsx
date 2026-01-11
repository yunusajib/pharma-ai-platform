'use client';

import { Card } from '@/components/ui/card';

interface ScoreCardProps {
  analysis: any;
}

export default function ScoreCard({ analysis }: ScoreCardProps) {
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-500 text-white';
      case 'yellow':
        return 'bg-yellow-500 text-white';
      case 'red':
        return 'bg-red-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const getProgressColor = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-500';
      case 'yellow':
        return 'bg-yellow-500';
      case 'red':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const renderProgressBar = (score: number, color: string) => {
    const percentage = (score / 5) * 100;
    return (
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div
          className={`h-full ${getProgressColor(color)} transition-all duration-1000 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    );
  };

  const overallPercentage = Math.round((analysis.overall_score / 5) * 100);

  return (
    <Card className="p-6 bg-white shadow-xl">
      {/* Overall Score */}
      <div className="mb-6 p-6 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-1">Overall Performance</h2>
            <p className="text-blue-100">
              {analysis.rep_name} with {analysis.doctor_name}
            </p>
          </div>
          <div className="text-right">
            <div className="text-5xl font-bold mb-1">
              {analysis.overall_score.toFixed(1)}
              <span className="text-2xl text-blue-200">/5.0</span>
            </div>
            <div className="text-lg text-blue-100">{overallPercentage}%</div>
          </div>
        </div>
        <div className="mt-4">
          {renderProgressBar(analysis.overall_score, analysis.overall_color)}
        </div>
      </div>

      {/* Individual Scores */}
      <h3 className="text-xl font-bold text-gray-900 mb-4">
        📊 Detailed Scorecard
      </h3>
      <div className="space-y-4">
        {Object.entries(analysis.scores).map(([key, scoreData]: [string, any]) => (
          <div key={key} className="border-b border-gray-200 pb-4 last:border-0">
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-gray-800">
                {scoreData.dimension}
              </span>
              <span
                className={`px-3 py-1 rounded-full text-sm font-bold ${getColorClasses(
                  scoreData.color
                )}`}
              >
                {scoreData.score.toFixed(1)}
              </span>
            </div>
            {renderProgressBar(scoreData.score, scoreData.color)}
            <p className="text-sm text-gray-600 mt-2">{scoreData.justification}</p>
            {scoreData.examples && scoreData.examples.length > 0 && (
              <div className="mt-2 space-y-1">
                {scoreData.examples.map((example: string, idx: number) => (
                  <div
                    key={idx}
                    className="text-xs bg-gray-50 p-2 rounded border-l-4 border-blue-400 italic text-gray-700"
                  >
                    "{example}"
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Summary */}
      {analysis.conversation_summary && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">📝 Conversation Summary</h4>
          <p className="text-sm text-blue-800">{analysis.conversation_summary}</p>
        </div>
      )}
    </Card>
  );
}
