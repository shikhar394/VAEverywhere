from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str


class UserPreference(BaseModel):
    product_type: str
    quantity: str
    is_priority: bool # TODO default to true
    delivery_address: str
    details: str
    preffered_brand: str

