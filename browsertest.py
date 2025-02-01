from playwright.async_api import async_playwright
import asyncio
import os

async def setup_persistent_browser():
    # Create a persistent profile directory
    user_data_dir = os.path.join(os.path.expanduser('~'), 'playwright_profile')
    user_data_dir = "~/Library/Application Support/Google/Chrome/Default"
    
    async with async_playwright() as playwright:
        # Launch persistent context
        browser_context = await playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,  # Set to True if you don't need UI
            args=[
                '--start-maximized',
                '--no-first-run',
                '--no-default-browser-check'
            ],
            viewport=None,  # Required for --start-maximized
            accept_downloads=True,
            locale='en-US',
            timeout=30000,
            
            # Optional: Configure additional preferences
            chromium_sandbox=False,
            slow_mo=50,  # Add delay between actions (in milliseconds)
            
            # Handle permissions
            permissions=['geolocation', 'notifications'],
            
            # # Configure specific domains for cookies/storage
            # storage_state={
            #     'cookies': [],
            #     'origins': []
            # }
        )
        
        # Create a new page in the context
        page = await browser_context.new_page()
        
        # Example: Navigate to a site and perform actions
        await page.goto('https://example.com')
        
        # Example: Save current storage state
        storage = await browser_context.storage_state(
            path="storage-state.json"  # Optional: save to file
        )
        
        # Keep the browser open for interaction
        await asyncio.sleep(30)  # Adjust time as needed
        
        # Clean up
        await browser_context.close()

# Run the browser setup
asyncio.run(setup_persistent_browser())
