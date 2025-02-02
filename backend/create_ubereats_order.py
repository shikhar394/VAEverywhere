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
class UberEatOrderConfig:
    openai_api_key: str
    chrome_path: str
    headless: bool = False
    model: str = "gpt-4o"

@dataclass
class OrderDetails:
    product_url: str
    product_quantity: str

@dataclass
class PlaceOrderConfig:
    openai_api_key: str
    chrome_path: str
    headless: bool = False
    priority: bool = True
    model: str = "gpt-4o"


def create_order_steps():
    steps = [
        "{index}. Navigate to {product_url} using the chrome address bar.",
        "{index}. Find and click the quantity button (look for attributes: 'button' and 'data-testid=\"quantity-selector\"').",
        "{index}. Click the quantity button and select {product_quantity}.",
        "{index}. Find and click the 'Add to Cart' button (look for attributes: 'button' and 'data-testid'='add-to-cart-button').\n\n"
    ]

    return steps

def place_order_steps():
    steps = [
        "{index}. Navigate to the Uber Eats checkout page on https://www.ubereats.com/ca/checkout using the chrome address bar.",
        "{index}. Find and click the edit address button (look for attributes: 'button' and 'data-testid='data-testid='edit-delivery-address-button'",
        "{index}. Select the address that reads 276 Queen St W, Toronto, ON M5V 3A3",
        "{index}. Select the priority option on the page (look for attributes: 'button')",
    ]

    return steps


def all_order_steps(order_details: list[OrderDetails]):
    steps = []

    index = 0
    for order in order_details:
        for step in create_order_steps():
            index += 1
            steps.append(step.format(index=index, product_url=order.product_url, product_quantity=order.product_quantity))

    for step in place_order_steps():
        index += 1
        steps.append(step.format(index=index))

    return "\n".join(steps)


def create_uber_eat_order_agent(config: UberEatOrderConfig, order_details: list[OrderDetails]):
    llm = ChatOpenAI(model=config.model, api_key=config.openai_api_key)

    browser = Browser(
        config=BrowserConfig(
            headless=config.headless,
            chrome_instance_path=config.chrome_path
        )
    )

    controller = Controller()

    order_steps = all_order_steps(order_details)

    print(order_steps)

    return Agent(
        task=f"""Follow the following steps closely to place an order for my alcohol.
            {order_steps}
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
    products = [
        {
            "product_url": "https://www.ubereats.com/ca/store/lcbo-49-spadina-avenue/wnsM8MsKWtCnjaQQ509Akg/efbc0fd0-6f52-5e25-8302-e4f65e54e938/33f28992-eebe-5ee8-9619-15260a64af77/0981ca0d-0e2e-51c4-b939-fff542398a51?storeSearchQuery=jutsu",
            "quantity": 5
        },
        {
            "product_url": "https://www.ubereats.com/ca/store/lcbo-49-spadina-avenue/wnsM8MsKWtCnjaQQ509Akg/efbc0fd0-6f52-5e25-8302-e4f65e54e938/33f28992-eebe-5ee8-9619-15260a64af77/855a3494-1d0d-5a9c-a780-68a27a570621?storeSearchQuery=jutsu",
            "quantity": 6
        }
    ]

    order_details = [OrderDetails(product_url=product["product_url"], product_quantity=product["quantity"]) for index, product in enumerate(products)]

    config = UberEatOrderConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", # This is for MacOS (Chrome)
    )
    agent = create_uber_eat_order_agent(config, order_details)
    asyncio.run(place_order(agent))

if __name__ == "__main__":
    main()