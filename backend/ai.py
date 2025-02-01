from openai import OpenAI
from models import User_Preference, Product_format
import os
from typing import List

class AI:
    def __init__(self):
        #self.api_key = os.getenv("OPEN_AI_KEY")
        if not self.api_key:
            print("API KEY: ", self.api_key)

            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            print(f"Error initializing OpenAI client: {str(e)}")
            raise
        
        self.model = "gpt-4o"
        self.system_prompt = """
You are a helpful assistant that helps people with ordering food, groceries, and adult products online.
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
Try not to be annoying and ask only the necessary questions. If the user does not provide information after first request, assume they do not have a preference.
Do not overwhelm the user with too many questions at once. Ask only one or two related questions each time.
"""
        self.messages = [
            {"role": "system", "content": self.system_prompt},
        ]

    def get_response(self, messages):
        try:
            formatted_messages = [self.messages[0]]
            for msg in messages:
                formatted_message = {
                    "role": msg.role,
                    "content": msg.content
                }
                print("FORMATTED MESSAGE: ", formatted_message)
                formatted_messages.append(formatted_message)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                stream=False
            )
            print("RESPONSE: ", response)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            raise

    async def get_preferences(self, messages: any) -> User_Preference:
        #formatted_content = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        #import pdb; pdb.set_trace()
        print("FORMATTED CONTENT: ", messages)
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Given the chat history, extract the user order preferences.",
                },
                {
                    "role": "user",
                    "content": messages,
                },
            ],
            response_format=User_Preference,
        )
        print("COMPLETION: ", completion)
        
        return completion.choices[0].message.parsed
    
    def make_decision(self, instruction: str, documents: str) -> Product_format:
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are an assistant and need to make a decision based on the following discription: {instruction}"},
                {"role": "user", "content": f"Which product should I buy from this list: {documents}"},
            ],
            response_format=Product_format,
        )
        return completion.choices[0].message.parsed

    def is_order_complete(self, content: str) -> bool:
        return "order info done" in content.lower()
