from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from models import Message, ChatRequest, ChatResponse
from helpers import generate_response_stream
from ai import AI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#--------_ENDPOINTS_--------
@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        ai = AI()
        response = ai.get_response(request.messages)
        print("RESPONSE in main: ", response)
        return {"response": response}
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )