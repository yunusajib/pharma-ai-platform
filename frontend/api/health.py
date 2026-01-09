from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mangum import Mangum
import time

app = FastAPI()

@app.get("/api/health")
def health_check():
    return JSONResponse({
        "status": "healthy",
        "version": "1.0.0",
        "openai_configured": True,
        "timestamp": time.time()
    })

handler = Mangum(app)
