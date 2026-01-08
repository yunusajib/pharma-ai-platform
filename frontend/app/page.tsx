import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Calendar, MessageSquare, FileText, TrendingUp } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
    return (
        <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 p-4 md:p-8">
            {/* Header */}
            <div className="max-w-6xl mx-auto mb-8">
                <div className="flex items-center justify-between mb-2">
                    <h1 className="text-3xl font-bold text-slate-900">Pharma Sales AI</h1>
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                        Demo Mode
                    </Badge>
                </div>
                <p className="text-slate-600">AI-powered compliance-first sales enablement</p>
            </div>

            <div className="max-w-6xl mx-auto">
                {/* Welcome Section */}
                <Card className="mb-6 border-blue-200 bg-blue-50">
                    <CardHeader>
                        <CardTitle className="text-blue-900">👋 Welcome, Sarah</CardTitle>
                        <CardDescription className="text-blue-700">
                            You have 4 calls scheduled today
                        </CardDescription>
                    </CardHeader>
                </Card>

                {/* Quick Actions */}
                <div className="mb-8">
                    <h2 className="text-xl font-semibold text-slate-900 mb-4">🎯 Quick Actions</h2>

                    <div className="grid md:grid-cols-2 gap-4">
                        {/* Pre-Call Prep */}
                        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-blue-200">
                            <CardHeader>
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                                        <Calendar className="w-6 h-6 text-blue-600" />
                                    </div>
                                    <div>
                                        <CardTitle className="text-lg">Prepare for Next Call</CardTitle>
                                        <CardDescription>Dr. Martinez • 10:30 AM • Cardiology</CardDescription>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <Button className="w-full bg-blue-600 hover:bg-blue-700">
                                    Start Preparation
                                </Button>
                            </CardContent>
                        </Card>

                        {/* Real-Time Q&A - WITH LINK */}
                        <Link href="/qa">
                            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                                <CardHeader>
                                    <div className="flex items-center gap-3">
                                        <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                                            <MessageSquare className="w-6 h-6 text-purple-600" />
                                        </div>
                                        <div>
                                            <CardTitle className="text-lg">Ask a Question</CardTitle>
                                            <CardDescription>Get real-time support during calls</CardDescription>
                                        </div>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <Button variant="outline" className="w-full">
                                        Open Q&A
                                    </Button>
                                </CardContent>
                            </Card>
                        </Link>

                        {/* Documentation */}
                        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                            <CardHeader>
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                                        <FileText className="w-6 h-6 text-green-600" />
                                    </div>
                                    <div>
                                        <CardTitle className="text-lg">Log Last Call</CardTitle>
                                        <CardDescription>Quick documentation</CardDescription>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <Button variant="outline" className="w-full">
                                    Create Notes
                                </Button>
                            </CardContent>
                        </Card>

                        {/* Insights */}
                        <Card className="hover:shadow-lg transition-shadow">
                            <CardHeader>
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                                        <TrendingUp className="w-6 h-6 text-orange-600" />
                                    </div>
                                    <div>
                                        <CardTitle className="text-lg">Today's Insights</CardTitle>
                                        <CardDescription>Territory performance</CardDescription>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-2 text-sm">
                                    <div className="flex justify-between">
                                        <span className="text-slate-600">Call Success Rate</span>
                                        <span className="font-semibold text-green-600">75%</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-600">vs. Target</span>
                                        <span className="font-semibold">68% avg</span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>

                {/* AI Agents Status */}
                <Card>
                    <CardHeader>
                        <CardTitle>🤖 AI Agents Available</CardTitle>
                        <CardDescription>Multi-agent system ready to assist</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid md:grid-cols-3 gap-3">
                            <div className="flex items-center gap-2 p-3 bg-green-50 rounded-lg">
                                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-sm font-medium text-green-900">Sales Agent</span>
                            </div>
                            <div className="flex items-center gap-2 p-3 bg-green-50 rounded-lg">
                                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-sm font-medium text-green-900">Medical Agent</span>
                            </div>
                            <div className="flex items-center gap-2 p-3 bg-green-50 rounded-lg">
                                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-sm font-medium text-green-900">Compliance Guardian</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Footer */}
                <div className="mt-8 text-center text-sm text-slate-500">
                    <p>Portfolio Project • Built with Next.js, FastAPI, CrewAI, GPT-4o</p>
                    <p className="mt-1">Compliance-First AI for Regulated Industries</p>
                </div>
            </div>
        </div>
    );
}
