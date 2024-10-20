from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)
# openai.api_key = api_key

dialogue_history_list = [{"role": "assistant", "content": "Hi, how can I assist you today?"}]

def conversation():
    instruction = """
        Task Description:
        You are simulating a conversation as an airline chatbot. Your job is to identify and respond to the customer's needs, available functions are only limited to searching for available flights, booking tickets, requesting refunds, or exchanging tickets.
        perform step by step.
        Steps:
        1. Determine the customer's need (search flights, book tickets, refund, or exchange).
        2. Collect the necessary information based on the request by asking the information one by one:

        - **Available Tickets**: departure location, destination, departure date, number of passengers.
        - **Booking Tickets**: all info for available tickets, plus customer name, ID, 16-digit card number, expiration date (MM/YY), and 3-digit CVV.
        - **Refund**: user ID, name, passport number, order ID.
        - **Exchange**: same as refund, plus new flight details (departure, destination, date, passengers), and payment info (card number, expiration date, CVV).

        3. After gathering all details, present the information back to the customer for confirmation and allow changes if needed.

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
 
            )
            content = response.choices[0].message.content
            # content = json.loads(content)
            print(f"Chatbot: {content}")
            messages.append({"role": "assistant", "content": content})
        except Exception as e:
            print(e)
            time.sleep(0.5)

if __name__ == "__main__":
    conversation()
