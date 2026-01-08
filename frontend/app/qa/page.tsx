"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, CheckCircle, Loader2, MessageSquare, ArrowLeft } from "lucide-react";
import { apiClient, QueryResponse } from "@/lib/api";
import Link from "next/link";

export default function QAPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!query.trim()) {
      setError("Please enter a question");
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await apiClient.sendQuery({
        query: query,
        user_id: "sarah_demo_user",
        hcp_context: {
          name: "Dr. Martinez",
          specialty: "Cardiology"
        }
      });

      setResponse(result);
    } catch (err) {
      setError("Failed to get response. Make sure the backend is running at http://localhost:8000");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <Link href="/">
            <Button variant="ghost" size="sm" className="mb-4">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-slate-900 mb-2">💬 Ask AI Anything</h1>
          <p className="text-slate-600">Get real-time, compliance-checked answers</p>
        </div>

        {/* Input Card */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5" />
              Your Question
            </CardTitle>
            <CardDescription>
              Ask about drug information, HCP objections, or competitive positioning
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea
              placeholder="Example: How do I handle side effect questions from Dr. Martinez?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              className="min-h-[100px]"
              disabled={loading}
            />

            <Button
              onClick={handleSubmit}
              disabled={loading || !query.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                "Get AI Response"
              )}
            </Button>

            {/* Example questions */}
            <div className="pt-4 border-t">
              <p className="text-sm text-slate-600 mb-2">Try these examples:</p>
              <div className="flex flex-wrap gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setQuery("How does our drug interact with warfarin?")}
                  disabled={loading}
                >
                  Drug interactions
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setQuery("Dr. Smith says our drug is too expensive. What do I say?")}
                  disabled={loading}
                >
                  Pricing objection
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setQuery("Can I use this for migraine prevention?")}
                  disabled={loading}
                  className="border-orange-300 text-orange-700"
                >
                  Off-label (will block)
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Card className="mb-6 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
                <div>
                  <p className="font-semibold text-red-900">Error</p>
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Response Display */}
        {response && (
          <div className="space-y-4">
            {/* Compliance Status */}
            <Card className={response.compliance_status.status === "BLOCKED" ? "border-red-300 bg-red-50" : "border-green-300 bg-green-50"}>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  {response.compliance_status.status === "APPROVED" ? (
                    <>
                      <CheckCircle className="w-6 h-6 text-green-600" />
                      <div>
                        <p className="font-semibold text-green-900">✅ Compliance: APPROVED</p>
                        <p className="text-sm text-green-700">This response is safe to use</p>
                      </div>
                    </>
                  ) : (
                    <>
                      <AlertCircle className="w-6 h-6 text-red-600" />
                      <div>
                        <p className="font-semibold text-red-900">⚠️ Compliance: BLOCKED</p>
                        <p className="text-sm text-red-700">{response.compliance_status.explanation}</p>
                      </div>
                    </>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* AI Response */}
            <Card>
              <CardHeader>
                <CardTitle>🤖 AI Response</CardTitle>
                <CardDescription>
                  Processed by: {response.agents_used.join(", ")}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="prose prose-slate max-w-none">
                  <div className="whitespace-pre-wrap text-slate-700">
                    {response.response}
                  </div>
                </div>

                {/* Metadata */}
                <div className="mt-6 pt-4 border-t flex items-center justify-between text-sm text-slate-600">
                  <div className="flex items-center gap-4">
                    <span>⚡ Response time: {response.response_time_seconds}s</span>
                    <span>🤖 Agents: {response.agents_used.length}</span>
                  </div>
                  <Badge variant="outline" className={
                    response.compliance_status.status === "APPROVED"
                      ? "bg-green-50 text-green-700 border-green-200"
                      : "bg-red-50 text-red-700 border-red-200"
                  }>
                    {response.compliance_status.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}