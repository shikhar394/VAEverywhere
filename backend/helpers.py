import asyncio
#Function to generate a streaming response
async def generate_response_stream(messages):
    response_text = "This where the response should be generated"
    for char in response_text:
        yield f"data: {char}\n\n"
        await asyncio.sleep(0.05)  # Simulate delay
    yield "data: [DONE]\n\n"
