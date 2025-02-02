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
    url: str

class Products(BaseModel):
	prods: List[Product]

async def create_uber_eat_agent(config: UberEatConfig):
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

    agent = Agent(
        task=f"""Navigate to Uber Eats and help me find all the beer options.

        Here are the specific steps:

        1. Navigate to {config.base_url} using the chrome address bar.
        2. Search LCBO in the website search bar and click on the first option that says LCBO
        3. Search "beer" in the website search bar that says Search LCBO (look for attributes: 'input' and id=\"search-suggestions-typeahead-input\") and select the first option that only says beer.
        4. For each product, extract product_name, price, details, size, and the quick view link for the product (href embedded under <a> tag for quick views)
        
        Important:
        - Wait for each element to load before interacting
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
            {"role": "user", "content": f"Please format the data in the specified format: {web_content}"}
        ],
        response_format=Products,
    )

    breakpoint()

    with open('options.json', 'w') as f:
        json.dump(completion.choices[0].message.parsed.prods, f)

    breakpoint()

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
    agent = asyncio.run(create_uber_eat_agent(config))
    asyncio.run(place_order(agent))

if __name__ == "__main__":
    main()
