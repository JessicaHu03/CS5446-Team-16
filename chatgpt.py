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
    instruction = f"""
        Task Description:
        You are simulating a conversation as an airline chatbot. Your job is to identify and respond to the customer's needs, available functions are only limited to searching for available flights, booking tickets, requesting refunds, or exchanging tickets.
        perform step by step.
        Steps:
        1. Ask user what the purpose of the conversation is.
        2. No matter what the user says first, collect the necessary information based on the request by asking the information one by one, in order to avoid ambiguity.:

        - **Search Available Tickets**: departure location, destination, departure date, number of passengers.
        - **Booking Tickets**: all info for available tickets, plus customer name, ID, 16-digit card number, expiration date (MM/YY), and 3-digit CVV.
        - **Refund**: user ID, name, passport number, order ID.
        - **Exchange**: same as refund, plus new flight details (departure, destination, date, passengers), and payment info (card number, expiration date, CVV).
        Note that you can only ask user the above information, no other information should be asked.
        3. After gathering all details, present the information back to the customer for confirmation and allow changes if needed by including the keyword 'confirm' in your response.
        """
    messages = [{
        "role": "system",
        "content": instruction
    }] + dialogue_history_list
    # print(f"Chatbot: No problem, I'll assist you to {purpose} flights.")
    
    collected_info = {}  # Dictionary to hold collected information
    print("Chatbot: Enter hello to start the conversation.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("End conversation.")
            break
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.2,
                timeout=30,
                messages=messages,
            )
            
            content = response.choices[0].message.content
            print(f"Chatbot: {content}")
            messages.append({"role": "assistant", "content": content})
            
            # Ask for confirmation if all necessary information is collected
            if "confirm" in content.lower():
                confirmation = input("User (confirm/yes): ").lower()
                if confirmation == "confirm" or confirmation == "correct" or confirmation == "yes":
                    print("Chatbot: Thank you! The information has been confirmed.")
                    # Collect information into a JSON format
                    return messages[-1]["content"]

        except Exception as e:
            print(e)
            time.sleep(0.5)

def extract_information(content):
    
    instruction = f"""
        Extract the information from the given content and return it in JSON format.
        Only extract the information, do not add any other words or phrases.
        Omit the information that is not necessary.
        The content given is: {content}
    """
    messages = [{
        "role": "system",
        "content": instruction
    }]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            timeout=30,
            messages=messages,
        )
        content = response.choices[0].message.content
        # print(content)
        return content
    except Exception as e:
        print(e)
        time.sleep(0.5)
if __name__ == "__main__":
    information = conversation()
    extracted_information = extract_information(information)
    print(extracted_information)
