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
import json
from fetch_ubereats_options import fetch_uber_eat_options, UberEatConfig
import os
import asyncio
from create_ubereats_order import order_driver
load_dotenv()
import subprocess

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
    
def kill_chrome():
    try:
        subprocess.run(["pkill", "-f", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"], check=True)
    except Exception as e:
        print(f"Error in pkill: {str(e)}")

@app.post("/preferences")
def preferences_endpoint(request: dict):
    ai = AI()
    # response_user_preferences = await ai.get_preferences(request["content"])
    # response_user_preferences_json = change_format_to_json_user_preferences(response_user_preferences)
    # print("RESPONSE in preferences: ", response_user_preferences_json)

    # response_test_data = ai.generate_test_data(response_user_preferences)
    # print("RESPONSE in test data: ", response_test_data)
    #pdb.set_trace()
    response_user_preferences_json = {'product Type': 'beer',
        'quantity': 'enough for 30 people',
        'isPriority': False,
        'deliveryAddress': '276 queen street',
        'personalPreference': 'want something from lcbo',
        'prefferedBrand': ''
    }

    kill_chrome()

    config = UberEatConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", # This is for MacOS (Chrome)
        search_term="lcbo beer",
        message="lcbo",
        base_url="https://www.ubereats.com/ca/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMkJlZXJ0b3duJTIwUHVibGljJTIwSG91c2UlMjBUb3JvbnRvJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyNTNjMDNmMjgtMzQxYi00MGZmLWI2YWMtMzA1ZTAzMmY1Mjc1JTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMnViZXJfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0E0My42NDYwMjg2JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTc5LjM4NDQzNjQlN0Q%3D",
        user_preferences="prefered_brand='Corona'",
    )
    # agent = asyncio.run(fetch_uber_eat_options(config))

    # kill_chrome()

    with open('products.json', 'r') as f:
        response_test_data = json.load(f)

    from pprint import pprint
    pprint(response_test_data)

    pprint(response_user_preferences_json)

    response_decision = ai.make_decision(change_format_to_string(response_user_preferences_json), change_format_to_string(response_test_data))

    formatted_products = []
    for product in response_decision.products:
        formatted_product = {
            "product_url": product.url,
            "quantity": product.number_packages
        }
        formatted_products.append(formatted_product)

    print("RESPONSE in decision: ", formatted_products)

    order_driver(formatted_products)

    return {"response": "ok"}


if __name__ == "__main__":
    preferences_endpoint({})
