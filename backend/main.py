from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from models import Message, ChatRequest
import asyncio
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#--------_FUNCTIONS_--------
#Function to generate a streaming response
async def generate_response_stream(messages):
    response_text = "This where the response should be generated"
    for char in response_text:
        yield f"data: {char}\n\n"
        await asyncio.sleep(0.05)  # Simulate delay
    yield "data: [DONE]\n\n"



#--------_ENDPOINTS_--------
@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        return StreamingResponse(
            generate_response_stream(request.messages),
            media_type='text/event-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))