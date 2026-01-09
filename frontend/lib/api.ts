// API client - now calls same-domain Vercel functions (NO CORS!)

const API_BASE_URL = ''; // Empty = same domain

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

class PharmaAIClient {
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    async healthCheck(): Promise<{ status: string; version: string }> {
        const response = await fetch(`${this.baseUrl}/api/health`);
        if (!response.ok) {
            throw new Error('Health check failed');
        }
        return response.json();
    }

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

export const apiClient = new PharmaAIClient();
// API client - calls Next.js API routes (which proxy to Render)
// This avoids CORS because browser -> Next.js (same domain)

const API_BASE_URL = ''; // Empty = same domain

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

class PharmaAIClient {
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    async healthCheck(): Promise<{ status: string; version: string }> {
        const response = await fetch(`${this.baseUrl}/api/health`);
        if (!response.ok) {
            throw new Error('Health check failed');
        }
        return response.json();
    }

    async getAgentStatus(): Promise<AgentsResponse> {
        const response = await fetch(`${this.baseUrl}/api/agents/status`);
        if (!response.ok) {
            throw new Error('Failed to fetch agent status');
        }
        return response.json();
    }

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

export const apiClient = new PharmaAIClient();