import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // NEW RENDER URL!
    const response = await fetch('https://pharma-ai-backend-1dlq.onrender.com/health');
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { status: 'unhealthy', error: 'Backend unavailable' },
      { status: 500 }
    );
  }
}
