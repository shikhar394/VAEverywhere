from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent, Controller
from dataclasses import dataclass
import json
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
load_dotenv()

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
cleaner_agent = OpenAI()

@dataclass
class UberEatConfig:
    openai_api_key: str
    chrome_path: str
    search_term: str
    message: str
    user_preferences: str
    headless: bool = False
    model: str = "gpt-4o-mini"
    base_url: str = "https://www.ubereats.com/ca/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjM1JTIwTWFyaW5lciUyMFRlcnIlMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjIxMDgwODRhZi1lMzc1LTE4ZmEtMGZhNi1lYjA0OWI3Yzk0OGUlMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIydWJlcl9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTQzLjYzOTczNTUlMkMlMjJsb25naXR1ZGUlMjIlM0EtNzkuMzkyMDg1NCU3RA%3D%3D"

class Product(BaseModel):
    product_name: str
    price: str
    details: str
    quantity: Optional[int]
    quick_view_url: str

class Products(BaseModel):
	prods: List[Product]

async def fetch_uber_eat_options(config: UberEatConfig):
    llm = ChatOpenAI(model=config.model, api_key=config.openai_api_key)

    browser = Browser(
        config=BrowserConfig(
            headless=config.headless,
            chrome_instance_path=config.chrome_path
        )
    )

    controller = Controller(output_model=Product)

    # 4. Find and click the "Search" button (look for attributes: 'button' and 'data-testid="multi-vertical-desktop-global-search-bar-wrapper"')
    # Create the agent with detailed instructions
    # 1. Navigate to {config.base_url} using the chrome address bar.
    # 2. Search LCBO in the website search bar and click on the first option that says LCBO
    # 3. Search "beer" in the website search bar that says Search LCBO (look for attributes: 'input' and id=\"search-suggestions-typeahead-input\") and click on the first option that only says beer.
    
    agent = Agent(
        task=f"""Navigate to Uber Eats and help me find all the beer options.

        Here are the specific steps:

        1. Navigate to https://www.ubereats.com/ca/store/lcbo-272-queen-st-w/htrZejmKU1WBA_E9oy1xAg?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjI3NiUyMFF1ZWVuJTIwU3QlMjBXJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyODFhY2NjNGEtZThjNC1kMWIyLTBlMmMtYzAzZDg0OTIzYWJjJTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMnViZXJfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0E0My42NDk3MzQ3JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTc5LjM5MjQ3ODQlN0Q%3D&sc=SEARCH_SUGGESTION&storeSearchQuery=beer using the chrome address bar.
        2. For each product, read the product_name, price, details, size, and the quick view link for the product (href embedded under <a> tag for quick views).
        
        Important:
        - Wait for each element to load before interacting
        - Follow the commands very carefully.
        - Remember the goal is to find options for the user.
        """,
        llm=llm,
        controller=controller,
        browser=browser,
    )

    result = await agent.run()
    # get the scraped content
    index = sorted([(a, len(b.extracted_content)) for (a, b) in enumerate(result.action_results())], key=lambda x: x[1], reverse=True)[0][0]
    web_content = result.action_results()[index].extracted_content.split("*")

    completion = cleaner_agent.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": f"You're a sales expert. The input is a list of strings with information about different products. Extract the following info as in the format specified."""},
            {"role": "user", "content": f"Extract the data for product name, price, details, quantity, and url for the quick view link for each product. {web_content}"}
        ],
        response_format=Products,
    )

    for prod in completion.choices[0].message.parsed.prods:
        details = prod.details
        detail_components = details.split("•")
        if len(detail_components) == 3:
            if "ct" in detail_components[0]:
                prod.quantity = int(detail_components[0].split(" ")[0])
        else:
            prod.quantity = 1
        prod.quick_view_url = "https://www.ubereats.com/ca" + prod.quick_view_url

    products = Products(prods=completion.choices[0].message.parsed.prods)

    with open('products.json', 'w') as f:
        f.write(products.model_dump_json())

async def place_order(agent: Agent):
    try:
        await agent.run(max_steps=100)
        agent.create_history_gif()
        print("Order placed successfully!")
    except Exception as e:
        print(f"Error placing order: {str(e)}")

@dataclass
class UserPreference:
    product_type: str
    quantity: str
    is_priority: bool
    delivery_address: str
    details: str
    prefered_brand: str


def main():
    config = UberEatConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", # This is for MacOS (Chrome)
        search_term="lcbo beer",
        message="lcbo",
        base_url="https://www.ubereats.com/ca/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMkJlZXJ0b3duJTIwUHVibGljJTIwSG91c2UlMjBUb3JvbnRvJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyNTNjMDNmMjgtMzQxYi00MGZmLWI2YWMtMzA1ZTAzMmY1Mjc1JTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMnViZXJfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0E0My42NDYwMjg2JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTc5LjM4NDQzNjQlN0Q%3D",
        user_preferences="prefered_brand='Corona'",
    )
    agent = asyncio.run(fetch_uber_eat_options(config))
    # asyncio.run(place_order(agent))

if __name__ == "__main__":
    main()