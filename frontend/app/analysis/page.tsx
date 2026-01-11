'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ConversationAnalysis() {
  const [conversation, setConversation] = useState('');
  const [repName, setRepName] = useState('Sarah Johnson');
  const [doctorName, setDoctorName] = useState('Dr. Martinez');
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!conversation.trim()) {
      setError('Please enter a conversation to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const response = await fetch('/api/analyze-conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation,
          rep_name: repName,
          doctor_name: doctorName,
        }),
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze conversation');
    } finally {
      setLoading(false);
    }
  };

  const sampleConversation = `Rep: Good morning Dr. Martinez! Thanks for taking the time to meet with me today.

Dr: Morning. What can I do for you?

Rep: I wanted to discuss CardioStatin and how it might benefit your patients with hyperlipidemia. How have your patients been responding to their current treatments?

Dr: They're doing okay, but I'm seeing some adherence issues with the generic statins.

Rep: That's actually one of the key differentiators with CardioStatin. Our clinical data shows a 40% reduction in muscle-related side effects, which directly translates to better adherence rates.

Dr: That's interesting, but the cost is significantly higher than the generics.

Rep: That's a valid concern. When we look at total cost of care, CardioStatin becomes more cost-effective. The improved adherence means fewer cardiovascular events - we're seeing 30% fewer ER visits in our studies.

Dr: Do you have data specific to elderly patients?

Rep: Absolutely - in our subgroup analysis of patients over 65, we saw a 35% reduction in major adverse cardiac events. I'd love to send you the full study data.

Dr: Okay, send me that data.

Rep: Perfect. I'll email it by tomorrow. Can I follow up next Thursday at 2pm to discuss any questions?

Dr: Thursday at 2 works.

Rep: Thank you so much for your time today, Dr. Martinez.`;

  const loadSample = () => {
    setConversation(sampleConversation);
    setAnalysis(null);
  };

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green': return 'bg-green-500 text-white';
      case 'yellow': return 'bg-yellow-500 text-white';
      case 'red': return 'bg-red-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getProgressColor = (color: string) => {
    switch (color) {
      case 'green': return 'bg-green-500';
      case 'yellow': return 'bg-yellow-500';
      case 'red': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const renderProgressBar = (score: number, color: string) => {
    const percentage = (score / 5) * 100;
    return (
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className={`h-full ${getProgressColor(color)} transition-all duration-500`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📊 Conversation Intelligence
          </h1>
          <p className="text-lg text-gray-600">
            AI-powered analysis of sales conversations with actionable coaching
          </p>
        </div>

        {/* Input Section */}
        <Card className="p-6 mb-6 bg-white shadow-lg">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sales Rep Name
              </label>
              <input
                type="text"
                value={repName}
                onChange={(e) => setRepName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Enter rep name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Doctor Name
              </label>
              <input
                type="text"
                value={doctorName}
                onChange={(e) => setDoctorName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Enter doctor name"
              />
            </div>
          </div>

          <label className="block text-sm font-medium text-gray-700 mb-2">
            Conversation Transcript
          </label>
          <textarea
            value={conversation}
            onChange={(e) => setConversation(e.target.value)}
            className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono text-sm"
            placeholder="Paste conversation here..."
          />

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          <div className="flex gap-4 mt-4">
            <Button
              onClick={handleAnalyze}
              disabled={loading || !conversation.trim()}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg disabled:opacity-50"
            >
              {loading ? '⚙️ Analyzing...' : '🔍 Analyze Conversation'}
            </Button>
            <Button
              onClick={loadSample}
              className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg"
            >
              📚 Load Sample
            </Button>
          </div>
        </Card>

        {/* Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Overall Score */}
            <Card className="p-6 bg-white shadow-xl">
              <div className="p-6 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg text-white mb-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-2xl font-bold mb-1">Overall Performance</h2>
                    <p className="text-blue-100">{analysis.rep_name} with {analysis.doctor_name}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-5xl font-bold">
                      {analysis.overall_score.toFixed(1)}
                      <span className="text-2xl text-blue-200">/5.0</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Individual Scores */}
              <h3 className="text-xl font-bold mb-4">📊 Detailed Scorecard</h3>
              <div className="space-y-4">
                {Object.entries(analysis.scores).map(([key, scoreData]: [string, any]) => (
                  <div key={key} className="border-b pb-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">{scoreData.dimension}</span>
                      <span className={`px-3 py-1 rounded-full text-sm font-bold ${getColorClasses(scoreData.color)}`}>
                        {scoreData.score.toFixed(1)}
                      </span>
                    </div>
                    {renderProgressBar(scoreData.score, scoreData.color)}
                    <p className="text-sm text-gray-600 mt-2">{scoreData.justification}</p>
                  </div>
                ))}
              </div>
            </Card>

            {/* Strengths & Improvements */}
            <div className="grid md:grid-cols-2 gap-6">
              <Card className="p-6 bg-white shadow-lg">
                <h3 className="text-xl font-bold text-green-700 mb-4">✅ Strengths</h3>
                <ul className="space-y-2">
                  {analysis.strengths.map((strength: string, idx: number) => (
                    <li key={idx} className="flex items-start p-3 bg-green-50 rounded-lg">
                      <span className="text-green-600 mr-2">•</span>
                      <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              </Card>

              <Card className="p-6 bg-white shadow-lg">
                <h3 className="text-xl font-bold text-yellow-700 mb-4">⚠️ Areas for Improvement</h3>
                <ul className="space-y-2">
                  {analysis.improvements.map((improvement: string, idx: number) => (
                    <li key={idx} className="flex items-start p-3 bg-yellow-50 rounded-lg">
                      <span className="text-yellow-600 mr-2">•</span>
                      <span>{improvement}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            </div>

            {/* Coaching */}
            <Card className="p-6 bg-white shadow-lg">
              <h3 className="text-xl font-bold text-indigo-700 mb-4">💡 Coaching Recommendations</h3>
              <div className="space-y-4">
                {analysis.coaching.map((item: any, idx: number) => (
                  <div key={idx} className="border border-indigo-200 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-2">{item.issue}</h4>
                    <p className="text-gray-700 mb-2"><strong>Recommendation:</strong> {item.recommendation}</p>
                    <div className="p-3 bg-indigo-50 rounded italic text-gray-800">
                      "{item.example}"
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
