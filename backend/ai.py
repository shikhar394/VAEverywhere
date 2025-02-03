from openai import OpenAI
from models import User_Preference, Product_format, List_Products
import os
from typing import List

class AI:
    def __init__(self):
        #self.api_key = os.getenv("OPEN_AI_KEY")
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
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
    
    def make_decision(self, instruction: str, documents: str) -> List_Products:
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are an assistant and need to make a decision based on the following discription: {instruction}"},
                {"role": "user", "content": f"Give me products that I should buy from this list: {documents}. Make sure that the list of beers include irish and belgian origin beers. The total amount of products (calculate: quantity * number_packages) is enough for the number of people."},
            ],
            response_format=List_Products,
        )
        return completion.choices[0].message.parsed
    

    def generate_test_data(self) -> str:
        return {
            "Name": "Budweiser",
            "Price": "$3.75",
            "Package Size": "6",
            "Details": "473 ml • 5% ABV",
            "URL": "https://www.ubereats.com/ca/store/lcbo-15-york-street/X3oCP7ePVAegUp6WBA670g/949e830c-602c-51bd-8335-74d7513cb383/33f28992-eebe-5ee8-9619-15260a64af77/1aebb116-0449-5ccc-acff-62f4ebe742c1?storeSearchQuery=beer" 
        }




    def is_order_complete(self, content: str) -> bool:
        return "order info done" in content.lower()
    

