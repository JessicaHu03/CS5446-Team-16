from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "assistant", "content": "Hi there, how can I help you today?"},
        {'role': 'user', 'content': 'I would like to search for available tickets.'}
    ]
)

print(completion.choices[0].message.content)



dialogue_history_list = [{"role": "assistant", "content": "Hi, how can I assist you today?"}]
# messages role contains system, user, assistant. system == instruction, user == user, assistant == gpt


def conversation(dialogue_history):
    instruction = """Task Description:
You are tasked with simulating a conversation between a customer and an airline chatbot. Your role is to play the airline chatbot. First, you should determine the customer's need based on the conversation. The need may be to search available flights, book tickets, refund tickets, or exchange tickets.
After which, you should collect user's data based on different needs.
If the customer needs to search available tickets, you should collect the customer's departure location, destination, date, flight_class, number of passengers.

Response Format:
Please return your responses in the following JSON format: { "content": "Your response here" }
After collecting all needed user information, return the collected information in JSON format
"""
    messages = [{
        "role": "system",
        "content": instruction
    }] + dialogue_history_list
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("End conversation.")
            break
        messages.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.7,
                timeout=30,
                messages=messages,
                response_format={ "type": "json_object" }
            )
            content = response.choices[0].message.content
            content = json.loads(content)
            print(f"Chatbot: {content['content']}")
            messages.append({"role": "assistant", "content": content["content"]})
        except Exception as e:
            print(e)
            time.sleep(0.5)

if __name__ == "__main__":
    conversation(dialogue_history_list)
