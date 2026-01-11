'use client';

import { Card } from '@/components/ui/card';
import { useState } from 'react';

interface CoachingPanelProps {
  analysis: any;
}

export default function CoachingPanel({ analysis }: CoachingPanelProps) {
  const [expandedCoaching, setExpandedCoaching] = useState<number | null>(null);

  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* Strengths */}
      <Card className="p-6 bg-white shadow-lg">
        <h3 className="text-xl font-bold text-green-700 mb-4 flex items-center">
          <span className="text-2xl mr-2">✅</span>
          Strengths
        </h3>
        <ul className="space-y-3">
          {analysis.strengths.map((strength: string, idx: number) => (
            <li
              key={idx}
              className="flex items-start p-3 bg-green-50 rounded-lg border-l-4 border-green-500"
            >
              <span className="text-green-600 mr-2 font-bold">•</span>
              <span className="text-gray-800">{strength}</span>
            </li>
          ))}
        </ul>
      </Card>

      {/* Areas for Improvement */}
      <Card className="p-6 bg-white shadow-lg">
        <h3 className="text-xl font-bold text-yellow-700 mb-4 flex items-center">
          <span className="text-2xl mr-2">⚠️</span>
          Areas for Improvement
        </h3>
        <ul className="space-y-3">
          {analysis.improvements.map((improvement: string, idx: number) => (
            <li
              key={idx}
              className="flex items-start p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-500"
            >
              <span className="text-yellow-600 mr-2 font-bold">•</span>
              <span className="text-gray-800">{improvement}</span>
            </li>
          ))}
        </ul>
      </Card>

      {/* Coaching Recommendations */}
      <Card className="md:col-span-2 p-6 bg-white shadow-lg">
        <h3 className="text-xl font-bold text-indigo-700 mb-4 flex items-center">
          <span className="text-2xl mr-2">💡</span>
          Coaching Recommendations
        </h3>
        <div className="space-y-4">
          {analysis.coaching.map((item: any, idx: number) => (
            <div
              key={idx}
              className="border border-indigo-200 rounded-lg overflow-hidden"
            >
              <div
                className="p-4 bg-indigo-50 cursor-pointer hover:bg-indigo-100 transition-colors"
                onClick={() =>
                  setExpandedCoaching(expandedCoaching === idx ? null : idx)
                }
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <span className="w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-bold mr-3">
                      {idx + 1}
                    </span>
                    <h4 className="font-semibold text-gray-900">{item.issue}</h4>
                  </div>
                  <span className="text-indigo-600">
                    {expandedCoaching === idx ? '▼' : '▶'}
                  </span>
                </div>
              </div>

              {expandedCoaching === idx && (
                <div className="p-4 bg-white border-t border-indigo-200 animate-slideDown">
                  <div className="mb-3">
                    <div className="text-sm font-semibold text-gray-600 mb-1">
                      💡 Recommendation:
                    </div>
                    <p className="text-gray-800">{item.recommendation}</p>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-600 mb-1">
                      🗣️ Example Response:
                    </div>
                    <div className="p-3 bg-indigo-50 rounded border-l-4 border-indigo-500 italic text-gray-800">
                      "{item.example}"
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
