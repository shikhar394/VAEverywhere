from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from models import Message, ChatRequest, ChatResponse
from helpers import change_format, change_format_to_string, change_format_to_json_user_preferences
from ai import AI
from dotenv import load_dotenv
import pdb; 

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
    
@app.post("/preferences")
async def preferences_endpoint(request: dict):
    print("REQUEST in preferences: ", request)
    ai = AI()
    response_user_preferences = await ai.get_preferences(request["content"])
    response_user_preferences_json = change_format_to_json_user_preferences(response_user_preferences)
    print("RESPONSE in preferences: ", response_user_preferences_json)
    #pdb.set_trace()

    response_test_data = ai.generate_test_data()
    print("RESPONSE in test data: ", response_test_data)
    #pdb.set_trace()

    response_decision = ai.make_decision(change_format_to_string(response_user_preferences_json), change_format_to_string(response_test_data))
    print("RESPONSE in decision: ", response_decision)

    response_decision_formatted = change_format(response_decision)
    print("RESPONSE in decision formatted: ", response_decision_formatted)

    return {"response": "ok"}
