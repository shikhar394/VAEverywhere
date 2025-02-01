from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()
model = "gpt-4o"

systemPrompt = """
You are a helpful assistant that helps people with ordering food and groceries online.
You job is to understand the user's request and their preferences.
You are also allowed to give recommendations and suggestions to the user.
You should ask the user for the necessary information to fulfill their request.
You should ask follow-up questions to clarify the user's request until you are able to answer all of the following questions:
1. What food or groceries do you want to order?
2. How many items do you want to order? or for how many people?
3. What is your delivery address?
4. Do you need priority delivery? (more expensive but faster)
5. Are there any specific brands or stores you prefer?
6. Do you have any other preferences or special requests?

Once you have all the necessary information, you should output the word "ORDER INFO DONE" and do not write anything else.
Try not to be annyoing and ask only the necessary questions. If the user does not provide information after first request, assume they do not have a preference.
Do not overwhelm the user with too many questions at once. Ask only one or two related questions each time.
"""

messages = [
    {"role": "system", "content": systemPrompt},
]
while True:
    userInput = input("You: ")
    messages.append({"role": "user", "content": userInput})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    if "order info done" in content.lower():
        break
    messages.append({"role": "assistant", "content": content})
    print("Bot:", content)
formattedContent = "\n".join([f"{m['role']}: {m['content']}" for m in messages])


class UserPreference(BaseModel):
    product_type: str
    quantity: str
    is_priority: bool
    delivery_address: str
    details: str
    preffered_brand: str


completion = client.beta.chat.completions.parse(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "Given the chat history, extract the user order preferences.",
        },
        {
            "role": "user",
            "content": formattedContent,
        },
    ],
    response_format=UserPreference,
)

preferences = completion.choices[0].message.parsed
print(preferences)
