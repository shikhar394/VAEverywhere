from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent, Controller
from dataclasses import dataclass
load_dotenv()

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

@dataclass
class UberEatConfig:
    openai_api_key: str
    chrome_path: str
    search_term: str
    message: str
    headless: bool = False
    model: str = "gpt-4o-mini"
    base_url: str = "https://www.ubereats.com/ca/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjM1JTIwTWFyaW5lciUyMFRlcnIlMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjIxMDgwODRhZi1lMzc1LTE4ZmEtMGZhNi1lYjA0OWI3Yzk0OGUlMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIydWJlcl9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTQzLjYzOTczNTUlMkMlMjJsb25naXR1ZGUlMjIlM0EtNzkuMzkyMDg1NCU3RA%3D%3D"
    user_preferences: str = "beer delicious"

def create_uber_eat_agent(config: UberEatConfig):
    llm = ChatOpenAI(model=config.model, api_key=config.openai_api_key)

    browser = Browser(
        config=BrowserConfig(
            headless=config.headless,
            chrome_instance_path=config.chrome_path
        )
    )

    controller = Controller()

    # 4. Find and click the "Search" button (look for attributes: 'button' and 'data-testid="multi-vertical-desktop-global-search-bar-wrapper"')
    # Create the agent with detailed instructions
    # return Agent(
    #     task=f"""Navigate to Uber Eats and search for the following term: {config.search_term}.

    #     Here are the specific steps:

    #     1. Navigate to {config.base_url} using the chrome address bar.
    #     2. Look for the text input field at the top of the page that says "Search Uber Eats?"
    #     3. Click the input field and type exactly this message:
    #     "{config.search_term}".
    #     4. Hit enter while in the input field.
    #     5. Click on the first division "data-testid=feed-shared-mini-store".
    #     6. Compile a list of beer options according to the criteria in {config.user_preferences}.
    #     7. For each beer option, print the beer name, store name, price, pack size and url of the specific beer in json format.
        
    #     Important:
    #     - Wait for each element to load before interacting
    #     - Make sure the message is typed exactly as shown
    #     - Verify the post button is clickable before clicking
    #     - Do not click on the '+' button which will add another tweet
    #     """,
    #     llm=llm,
    #     controller=controller,
    #     browser=browser,
    # )
    return Agent(
        task=f"""Navigate to Uber Eats and search for the following term: {config.search_term}.

        Here are the specific steps:

        1. Navigate to {config.base_url} using the chrome address bar.
        2. Look for the text input field at the top of the page that says "Search Uber Eats?"
        3. Click the input field and type exactly this message:
        "{config.search_term}".
        4. Hit enter while in the input field.
        5. Click on the first division "data-testid=feed-shared-mini-store".
        6. Compile a list of beer options according to the criteria in {config.user_preferences}.
        7. For each beer option, print the beer name, store name, price, pack size and url of the specific beer in json format.
        
        Important:
        - Wait for each element to load before interacting
        - Make sure the message is typed exactly as shown
        - Verify the post button is clickable before clicking
        - Do not click on the '+' button which will add another tweet
        """,
        llm=llm,
        controller=controller,
        browser=browser,
    )

async def place_order(agent: Agent):
    try:
        await agent.run(max_steps=100)
        agent.create_history_gif()
        print("Order placed successfully!")
    except Exception as e:
        print(f"Error placing order: {str(e)}")


def main():
    config = UberEatConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", # This is for MacOS (Chrome)
        search_term="beer",
        message="beer",
        # base_url="https://www.ubereats.com/ca/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjM1JTIwTWFyaW5lciUyMFRlcnIlMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjIxMDgwODRhZi1lMzc1LTE4ZmEtMGZhNi1lYjA0OWI3Yzk0OGUlMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIydWJlcl9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTQzLjYzOTczNTUlMkMlMjJsb25naXR1ZGUlMjIlM0EtNzkuMzkyMDg1NCU3RA%3D%3D",
        base_url="https://www.ubereats.com/ca/search?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMkJlZXJ0b3duJTIwUHVibGljJTIwSG91c2UlMjBUb3JvbnRvJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyNTNjMDNmMjgtMzQxYi00MGZmLWI2YWMtMzA1ZTAzMmY1Mjc1JTIyJTJDJTIycmVmZXJlbmNlVHlwZSUyMiUzQSUyMnViZXJfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0E0My42NDYwMjg2JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTc5LjM4NDQzNjQlN0Q%3D&q=beer&sc=SEARCH_BAR&searchType=GLOBAL_SEARCH&vertical=ALL",
        user_preferences="LCBO beer delicious",
    )
    agent = create_uber_eat_agent(config)
    asyncio.run(place_order(agent))

if __name__ == "__main__":
    main()
