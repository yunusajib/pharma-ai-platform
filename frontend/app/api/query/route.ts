import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    console.log('Proxying request to Render backend...');
    
    // Fetch with 60 second timeout (for Render wake-up)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000);
    
    const response = await fetch('https://pharma-ai-backend.onrender.com/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Backend error:', response.status, errorText);
      throw new Error(`Backend returned ${response.status}`);
    }

    const data = await response.json();
    console.log('Backend response received successfully');
    
    return NextResponse.json(data);
    
  } catch (error: any) {
    console.error('Proxy error:', error.message);
    
    if (error.name === 'AbortError') {
      return NextResponse.json(
        { error: 'Backend is waking up (free tier). This can take 30-60 seconds. Please try again.' },
        { status: 504 }
      );
    }
    
    return NextResponse.json(
      { error: `Proxy failed: ${error.message}` },
      { status: 500 }
    );
  }
}
