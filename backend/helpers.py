import asyncio
#Function to generate a streaming response
async def generate_response_stream(messages):
    response_text = "This where the response should be generated"
    for char in response_text:
        yield f"data: {char}\n\n"
        await asyncio.sleep(0.05)  # Simulate delay
    yield "data: [DONE]\n\n"


# Convert old product format to new product format
def change_format(old_dict):
  print("OLD DICT: ", old_dict)
  new_dict = {}
  new_dict['url'] = old_dict.url
  new_dict["quantity"] = old_dict.number_packages
  return new_dict

def change_format_to_string(data):
   return ", ".join(f"{key}: {value}" for key, value in data.items())

def change_format_to_json_user_preferences(user_preference):
    """Convert User_Preference object to JSON-compatible dictionary"""
    return {
        "product_type": user_preference.product_type,
        "quantity": user_preference.quantity,
        "is_priority": user_preference.is_priority,
        "delivery_address": user_preference.delivery_address,
        "details": user_preference.details,
        "preferred_brand": user_preference.preffered_brand  # Note: maintaining the misspelling from original
    }