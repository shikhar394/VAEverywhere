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
class PlaceOrderConfig:
    openai_api_key: str
    chrome_path: str
    headless: bool = False
    priority: bool = True
    model: str = "gpt-4o"

def place_uber_eat_order_agent(config: PlaceOrderConfig):
    llm = ChatOpenAI(model=config.model, api_key=config.openai_api_key)

    browser = Browser(
        config=BrowserConfig(
            headless=config.headless,
            chrome_instance_path=config.chrome_path
        )
    )

    controller = Controller()

    steps = [
        "1. Navigate to the Uber Eats checkout page on https://www.ubereats.com/ca/checkout using the chrome address bar.",
        "2. Find and click the edit address button (look for attributes: 'button' and 'data-testid='data-testid='edit-delivery-address-button'",
        "3. Select the address that reads 276 Queen St W, Toronto, ON M5V 3A3",
        "4. Select the priority option on the page (look for attributes: 'button')",
    ]

    steps = "\n".join(steps)

    return Agent(
        task=f"""Follow the following steps closely to place an order for my alcohol.

        {steps}
            
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
    config = PlaceOrderConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", # This is for MacOS (Chrome)
    )
    agent = create_uber_eat_order_agent(config)
    asyncio.run(place_order(agent))

if __name__ == "__main__":
    main()
