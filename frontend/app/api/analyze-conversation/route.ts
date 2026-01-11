import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';
export const maxDuration = 60;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    console.log('[ANALYSIS PROXY] Analyzing conversation...');
    
    const response = await fetch('https://pharma-ai-backend-1dlq.onrender.com/api/analyze-conversation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('[ANALYSIS PROXY] Backend error:', errorText);
      return NextResponse.json(
        { error: `Analysis failed: ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    console.log('[ANALYSIS PROXY] Analysis complete');
    
    return NextResponse.json(data);
    
  } catch (error: any) {
    console.error('[ANALYSIS PROXY] Error:', error);
    return NextResponse.json(
      { error: `Analysis proxy failed: ${error.message}` },
      { status: 500 }
    );
  }
}
