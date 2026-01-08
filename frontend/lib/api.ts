// API client for communicating with FastAPI backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Type definitions matching backend models
export interface QueryRequest {
    query: string;
    user_id: string;
    hcp_context?: {
        name?: string;
        specialty?: string;
    };
}

export interface ComplianceCheck {
    status: 'APPROVED' | 'BLOCKED';
    violation_type?: string;
    explanation?: string;
}

export interface QueryResponse {
    query: string;
    response: string;
    agents_used: string[];
    compliance_status: ComplianceCheck;
    response_time_seconds: number;
}

export interface AgentStatus {
    name: string;
    status: string;
    version: string;
}

export interface AgentsResponse {
    total_agents: number;
    agents: AgentStatus[];
    system_status: string;
}

// API Client Class
class PharmaAIClient {
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    // Health check
    async healthCheck(): Promise<{ status: string; version: string }> {
        const response = await fetch(`${this.baseUrl}/health`);
        if (!response.ok) {
            throw new Error('Health check failed');
        }
        return response.json();
    }

    // Get agent status
    async getAgentStatus(): Promise<AgentsResponse> {
        const response = await fetch(`${this.baseUrl}/api/agents/status`);
        if (!response.ok) {
            throw new Error('Failed to fetch agent status');
        }
        return response.json();
    }

    // Send query to backend
    async sendQuery(request: QueryRequest): Promise<QueryResponse> {
        const response = await fetch(`${this.baseUrl}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error('Query failed');
        }

        return response.json();
    }
}

// Export singleton instance
export const apiClient = new PharmaAIClient();

