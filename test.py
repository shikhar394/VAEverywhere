from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser
from browser_use.browser.context import BrowserContext
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()


async def main():
    browser = Browser()
    
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