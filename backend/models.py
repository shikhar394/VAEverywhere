from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str


class User_Preference(BaseModel):
    product_type: str
    quantity: str
    is_priority: bool # TODO default to true
    delivery_address: str
    details: str
    preffered_brand: str

class Product_format(BaseModel):
  brand: str
  url: str
  price: float
  package_size: int
  number_packages: int
  description: str


class List_Products(BaseModel):
    products: List[Product_format]
