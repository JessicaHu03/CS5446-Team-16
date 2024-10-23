from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time
import presentation.cli as cli

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

        - **Search Available Tickets**: departure location, destination, departure date (YYYY-MM-DD), flight class (First/Business/Economy), and number of passengers.
        - **Booking Tickets**: all info for available tickets
        - **Refund**: user ID, name, passport number, order ID.
        - **Exchange**: same as refund, plus new flight details (departure, destination, departure date (YYYY-MM-DD), new flight class (First/Business/Economy), new number of passengers), and payment info (card number, expiration date, CVV).
        Note that you can only ask user the above information, no other information should be asked. When asking for user specific information, do emphasize that the information will only be used for the purpose of this conversation.
        3. After gathering all details, present the information back to the customer for confirmation and allow changes if needed by including the keyword 'confirm' in your response. also add a key-value pair where key is "query", and purpose is the purpose of this conversation (available options are only search, book, refund, exchange) as the last row of the summary.
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
                confirmation = input("User (yes/no): ").lower()
                if confirmation == "confirm" or confirmation == "correct" or confirmation == "yes":
                    print("Chatbot: Thank you! The information has been confirmed.")
                    # Collect information into a JSON format
                    return messages[-1]["content"]

        except Exception as e:
            print(e)
            time.sleep(0.5)

def conversation_search(available_flight):
    instruction = f"""
        Task Description:
        You are simulating a conversation as an airline chatbot. The customer wants to search for available flights, the available flights are listed as {available_flight}.
        You should first omit the first, ninth, tenth and twelvth column, show the user flight information starting from the second column
        List and show the available flights and their details.
        The columns of the table are: flight id,departure location, destination, departure time, arrival time, flight duration, class, price.
        After that, end the conversation.
    """
    messages = [{
        "role": "system",
        "content": instruction
    }] + dialogue_history_list
    
    while True:
        
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
                confirmation = input("User (yes/no): ").lower()
                if confirmation == "confirm" or confirmation == "correct" or confirmation == "yes":
                    print("Chatbot: Thank you! The information has been confirmed.")
                    # Collect information into a JSON format
                    return messages[-1]["content"]

            user_input = input("User: ")
            if user_input.lower() == "exit":
                print("End conversation.")
                break
            messages.append({"role": "user", "content": user_input})
        except Exception as e:
            print(e)
            time.sleep(0.5)
    
    
def conversation_book(available_flight):
    
    instruction = f"""
        Task Description:
        You are simulating a conversation as an airline chatbot. The customer wants to search or book for available flights, the available flights are listed as {available_flight}.
        If there's no available flight (none), simply tell the user no flight found.
        If there's flight available,
        You should first omit the first, ninth, tenth and twelvth columns
        for example: given (2642, 'SQ876', 'Singapore', 'Taipei', '2024-11-12 08:10', '2024-11-12 12:55', 285, 'economy', 90, 0, 869.2, 0), you should only show ('SQ876', 'Singapore', 'Taipei', '2024-11-12 08:10', '2024-11-12 12:55', 285, 'economy', 869.2)
        List and show ALL the available flights.
        The columns of the table are: flight id,departure location, destination, departure time, arrival time, flight duration, class, price.
        
        Ask the user if there's flight he keens, if he does, ask for the following information one by one:
        - flight ID
        - user ID
        - user name
        - passport number
        - credit card number (16 digits)
        - expiry_date
        - cvv
        and set "book" = True
        Note that you can only ask user the above information, no other information should be asked. When asking for user specific information, do emphasize that the information will only be used for the purpose of this conversation.
        DO NOT change any information to * when confirming.
        After gathering all details, present the information back to the customer for confirmation and allow changes if needed by including the keyword 'confirm' in your response.
        
        If the user doesn't choose a flight, set "book" = False.
        
    """
    messages = [{
        "role": "system",
        "content": instruction
    }] + dialogue_history_list
    while True:
        
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
                confirmation = input("User (yes/no): ").lower()
                if confirmation == "confirm" or confirmation == "correct" or confirmation == "yes":
                    print("Chatbot: Thank you! The information has been confirmed.")
                    # Collect information into a JSON format
                    return messages[-1]["content"]

            user_input = input("User: ")
            if user_input.lower() == "exit":
                print("End conversation.")
                break
            messages.append({"role": "user", "content": user_input})
        except Exception as e:
            print(e)
            time.sleep(0.5)
    
    
def extract_information(content):
    
    instruction = f"""
        Extract the information from the given content and return it in JSON format.
        Only extract the information, do not add any other words or phrases.
        Omit the information that is not necessary.
        The content given is: {content}
        Only add the key-value pair for the information that is provided.
        The keys for each information should be:
        - query: purpose of the conversation (search, book, refund, exchange)
        - departure: departure location
        - destination: destination location
        - date: departure date (YYYY-MM-DD)
        - flight_class: flight class (First/Business/Economy) for both booking and exchange
        - num_passengers: number of passengers for both booking and exchange
        - user_id: user ID 
        - user_name: customer name
        - passport_num: passport number
        - flight_id: flight ID
        - card_number: 16-digit card number
        - expiry_date: expiration date (MM/YY)
        - cvv: 3-digit CVV
        - order_id: order ID
        
        DO NOT add ```json ``` in the response
    """
    messages = [{
        "role": "system",
        "content": instruction
    }]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.1,
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
    
    try:
        data_dict = json.loads(extracted_information)
        print("The information is valid JSON.")
        # if data_dict["query"] == "search":
        #     available_flight = cli.available_tickets(data_dict["departure"], data_dict["destination"], data_dict["date"], data_dict["flight_class"], data_dict["num_passengers"])
        #     book_flight = conversation_book(available_flight)
            
        if data_dict["query"] == "search" or data_dict["query"] == "book":
            available_flight = cli.available_tickets(data_dict["departure"], data_dict["destination"], data_dict["date"], data_dict["flight_class"], data_dict["num_passengers"])
            book_flight = conversation_book(available_flight)
            print("-----")
            print(book_flight)
            extracted_information_add = extract_information(book_flight)
            print("-----")
            print(extracted_information_add)
            data_dict_add = json.loads(extracted_information_add) # concat two dictionaries
            data_dict.update(data_dict_add)
            print("User information JSON updated")
            book_ticket = cli.book_ticket(data_dict["user_id"], data_dict["user_name"], data_dict["passport_num"], data_dict["flight_id"], data_dict["num_passengers"], data_dict["flight_class"], data_dict["card_number"], data_dict["expiry_date"], data_dict["cvv"])
        
        elif data_dict["query"] == "refund":
            cli.refund(data_dict["user_id"], data_dict["user_name"], data_dict["passport_num"], data_dict["order_id"])
        elif data_dict["query"] == "exchange":
            cli.exchange_ticket(data_dict["order_id"], data_dict["passport_num"], data_dict["user_id"], data_dict["departure"], data_dict["destination"], data_dict["date"], data_dict["flight_class"], data_dict["num_passengers"], data_dict["card_number"], data_dict["expiry_date"], data_dict["cvv"])

    except json.JSONDecodeError:
        print("The information is not valid JSON.")
    
