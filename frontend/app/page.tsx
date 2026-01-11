'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function Home() {
  const [agentStatus, setAgentStatus] = useState<any>(null);

  useEffect(() => {
    // Wake up backend on page load
    const wakeBackend = async () => {
      try {
        console.log('Waking up backend...');
        await fetch('/api/health', { method: 'GET' });
      } catch (e) {
        console.log('Backend wake-up initiated');
      }
    };
    
    wakeBackend();

    // Fetch agent status
    const fetchStatus = async () => {
      try {
        const response = await fetch('/api/agents/status');
        if (response.ok) {
          const data = await response.json();
          setAgentStatus(data);
        }
      } catch (error) {
        console.error('Failed to fetch agent status:', error);
      }
    };

    fetchStatus();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            💊 Pharma AI Platform
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Multi-Agent AI System for Pharmaceutical Sales
          </p>
          <p className="text-lg text-gray-500">
            Real-time compliance detection • Strategic sales guidance • Conversation intelligence
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-12">
          {/* Q&A Agent Card */}
          <Link href="/qa">
            <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer border-2 border-transparent hover:border-blue-500">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                AI Sales Assistant
              </h3>
              <p className="text-gray-600 mb-4">
                Get real-time strategic advice with automatic compliance checking
              </p>
              <div className="text-blue-600 font-semibold">
                Ask a Question →
              </div>
            </div>
          </Link>

          {/* Conversation Analysis Card */}
          <Link href="/analysis">
            <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer border-2 border-transparent hover:border-indigo-500">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Conversation Intelligence
              </h3>
              <p className="text-gray-600 mb-4">
                Analyze sales conversations with AI-powered scoring and coaching
              </p>
              <div className="text-indigo-600 font-semibold">
                Analyze Conversations →
              </div>
            </div>
          </Link>

          {/* Agent Status Card */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-4">⚙️</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              System Status
            </h3>
            {agentStatus ? (
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Sales Agent</span>
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    Active
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Compliance</span>
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    Active
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Analysis Agent</span>
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    Active
                  </span>
                </div>
              </div>
            ) : (
              <div className="text-gray-500">Loading status...</div>
            )}
          </div>
        </div>

        {/* Key Features */}
        <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            🎯 Key Features
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="flex items-start">
              <div className="text-2xl mr-3">✅</div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">
                  Real-time Compliance Detection
                </h4>
                <p className="text-gray-600 text-sm">
                  3-layer off-label detection prevents regulatory violations
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="text-2xl mr-3">🧠</div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">
                  Multi-Agent AI System
                </h4>
                <p className="text-gray-600 text-sm">
                  Orchestrated agents for sales strategy and compliance
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="text-2xl mr-3">⚡</div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">
                  Fast Response Times
                </h4>
                <p className="text-gray-600 text-sm">
                  8-12s AI responses, &lt;1s compliance blocking
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="text-2xl mr-3">📈</div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">
                  Performance Analytics
                </h4>
                <p className="text-gray-600 text-sm">
                  AI-powered conversation scoring and coaching
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Note */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>Powered by OpenAI GPT-4 • FastAPI • Next.js</p>
          <p className="mt-2">
            Backend hosted on Render free tier - first request may take 30s to wake up
          </p>
        </div>
      </div>
    </div>
  );
}
