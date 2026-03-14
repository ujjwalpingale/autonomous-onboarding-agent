import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import chat_with_agent

app = FastAPI(title="Autonomous Developer Onboarding Agent API")

# Setup CORS to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Onboarding Agent Backend"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives a message from the user and returns the AI's response.
    """
    ai_response = chat_with_agent(request.message, request.session_id)
    return ChatResponse(response=ai_response)

# Mount the frontend directory horizontally
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def serve_frontend():
    """Serves the main chat UI interface on root path"""
    return FileResponse("../frontend/index.html")
