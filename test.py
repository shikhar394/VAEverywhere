from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

import asyncio
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()


async def main():
    # Create a temporary directory for the persistent context
    user_data_dir = os.path.join(tempfile.gettempdir(), "playwright_dev_profile")
    
    # Browser context configuration
    config = BrowserConfig(
        headless=False,
        disable_security=True,
    )
    browser = Browser(config=config)

    async with await browser.new_context() as context:
        agent = Agent(
            task="Go to Reddit, search for 'browser-use', click on the first post and return the first comment.",
            llm=ChatOpenAI(model="gpt-4o-mini"),
            save_conversation_path="logs/conversation.json"
        )

    # Run the agent
    result = await agent.run()
    print(result)

    # Manually close the browser
    await browser.close()

asyncio.run(main())