from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time
import presentation.cli as cli

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

dialogue_history_list = None
status = None
available_flight = None
instruction = None
messages = None
user_info = {}
order_id = -1

def init():
    global instruction, status, messages, user_info, available_flight, order_id, dialogue_history_list
    dialogue_history_list = [{"role": "assistant", "content": "Hi, how can I assist you today?"}]
    status = 'select'
    available_flight = ""

    instruction = {
        'select': f"""
            Task Description:
            As an AI chatbot for an airline, your primary role is to assist customers by identifying their needs and providing support with specific functions. You can perform four main actions:
            Searching for available flights
            Booking tickets
            Requesting refunds
            Exchanging tickets
            
            Instructions:
            Identify the Customer's Intent:

            Analyze the customer's input to determine their purpose in the conversation. If the intent is clear, proceed with the relevant action.
            If the intent is unclear, ask follow-up questions to better understand their needs. Avoid making assumptions.
            Available Actions:

            Based on the identified intent, return one of the following keywords:
            search - for checking available flights.
            book - for booking tickets.
            refund - for refund requests.
            exchange - for ticket exchange requests.
            Handling Ambiguity:

            If the customer's input does not clearly indicate a specific action (e.g., they mention general travel plans without specific details), respond with clarifying questions to narrow down the scope of their request.
            Examples:
            If a customer says, “I need help with my flight,” ask if they are interested in a searching available flights, booking a new flight, or requesting support with refunds or exchanges.
            
            Expected Output:
            For each clear customer intent, return only the appropriate action keyword (search, book, refund, exchange) to indicate the function they need.
            Sample Responses:
            Customer: “I want to find flights to New York for next month.”
            Output: search
            Customer: “I need to change my flight to a later date.”
            Output: exchange
            """,
        'search': f"""
            Task Description:
            As an airline chatbot, your role is to guide the user in searching for available flights. When the user initiates a flight search, gather the following essential details:
            1. Departure Location - Where the user will depart from.
            2. Destination - Where the user wants to fly to.
            3. Departure Date - In the format YYYY-MM-DD. The date should fall within November 2024.
            4. Flight Class - Specify as First, Business, or Economy.
            5. Number of Passengers - The total number of passengers.
            
            Instructions:
            Request Information sequentially in order, unless multiple details can be provided in a single input for user.
            
            Prompt the user for each missing piece of information in a clear and concise manner.
            Example prompt: “Please provide the departure location, destination, departure date (YYYY-MM-DD), flight class (First/Business/Economy), and number of passengers.”
            Display Summary When Information is complete:

            Once All required details are gathered, display a summary of the information back to the user.
            Example summary:
            Departure Location: [User Input]
            Destination: [User Input]
            Departure Date: [User Input]
            Flight Class: [User Input]
            Number of Passengers: [User Input]
            Expected Behavior:

            After presenting the summary, wait for user confirmation before proceeding with any further steps 
            Sample Workflow:
            User: “I want to find flights.”
            Chatbot: “Great! Could you provide the departure location?”
            User: “New York”
            Chatbot: “And the destination?”
            User: “[Destination],” and so on until all information is collected.
            Chatbot (Summary): “To confirm, here's what I have: Departure from New York to [Destination] on [Date] in [Class] class for [Number of Passengers] passengers.”
            Ask the user to confirm by only typing "confirm" in the chatbot.
        """,
        'show_flight': "",
        'refund': f"""
            Task Description:
            As an airline chatbot, your role is to assist the user in requesting a refund for a booked ticket. First, gather the following essential details:
            User ID - The unique identifier assigned to the user.
            Name - The user's name as it appears on the ticket.
            Passport Number - The passport number associated with the booking.
            Order ID - The order or booking ID related to the ticket purchase.
            
            Instructions:
            Request Information Sequentially in order, unless multiple details can be provided in a single input for user.

            Prompt the user for each missing piece of information in a clear and concise manner.
            Once All required details are gathered, display a summary of the information back to the user.
            Example summary:
            User ID: [User Input]
            Name: [User Input]
            Passport Number: [User Input]
            Order ID: [User Input]
            
            After presenting the summary, wait for user confirmation before proceeding with any further steps 
            Ask the user to confirm by only typing "confirm" in the chatbot.
        """,
        'exchange': f"""
            Task Description:
            As an airline chatbot, your role is to assist the user in exchanging a ticket. First, gather the following essential details:
            User ID - The unique identifier assigned to the user.
            Name - The user's name as it appears on the ticket.
            Passport Number - The passport number associated with the booking.
            Order ID - The order or booking ID related to the ticket purchase.
            
            Instructions:
            Request Information Sequentially in order, unless multiple details can be provided in a single input for user.

            Prompt the user for each missing piece of information in a clear and concise manner.
            Once All required details are gathered, display a summary of the information back to the user.
            Example summary:
            User ID: [User Input]
            Name: [User Input]
            Passport Number: [User Input]
            Order ID: [User Input]
            
            After presenting the summary, wait for user confirmation before proceeding with any further steps 
            Ask the user to confirm by only typing "confirm" in the chatbot.
        """,
    }

    messages = [{"role": "system", "content": instruction[status]}]

    user_info = {}
    order_id = -1

def interface(user_input):
    llm_output = None
    global instruction, status, messages, user_info, available_flight, order_id
    confirm_keyword = ["confirm", "correct", "yes"]

    if status == 'select':
        llm_output = conversation("I want to " + user_input)
        if llm_output in ['search', 'book', 'refund', 'exchange']:
            status = llm_output
            if status == 'search' or status == 'book':
                messages = [{"role": "system", "content": instruction['search']}] # init message
            else:
                messages = [{"role": "system", "content": instruction[status]}] # init message

    if status == 'search' or status == 'book' or status == 'exchange_search':
        
        if user_input.lower() in confirm_keyword:
            llm_output = "Please press any key to continue..."
            user_info.update(json.loads(extract_information(messages[-1]['content'])))
            # print(user_info)
            if status == 'exchange_search':
                status = 'exchange_show_flight'
            else:
                status = 'show_flight'
            
            available_flight = cli.available_tickets(user_info["departure"], user_info["destination"], user_info["date"], user_info["flight_class"], user_info["num_passengers"])
            # print(available_flight)
            if len(available_flight) == 0:
                llm_output = "Sorry, no flight available. If you need assistance in the future or want to search for flights again, feel free to ask. Have a great day!"
                status = 'done'
            
            else:
                instruction['show_flight'] = f"""
                Task Description:
                You are an airline chatbot. The available flights are {available_flight}.
                If there's flight available,
                You should omit the ninth, tenth and twelvth columns
                for example: given (2642, 'SQ876', 'Singapore', 'Taipei', '2024-11-12 08:10', '2024-11-12 12:55', 285, 'economy', 90, 0, 869.2, 0), you should only show (2642, 'SQ876', 'Singapore', 'Taipei', '2024-11-12 08:10', '2024-11-12 12:55', 285, 'economy', 869.2)
                List and show ALL the available flights.
                The columns of the table are: flight id, flight number, departure location, destination, departure time, arrival time, flight duration, class, price.
                If there's no available flight (none), simply tell the user no flight found.
                
                Ask the user if there's flight he keens, if he does, ask for the following information one by one:
                - flight ID
                - user ID (digits)
                - user name
                - passport number (digits)
                - credit card number (16 digits)
                - expiry_date (mm/yy)
                - cvv (3 digits)
                and set "book" = True
                Note that you can only ask user the above information, no other information should be asked. When asking for user specific information, do emphasize that the information will only be used for the purpose of this conversation.
                DO NOT change any information to * when confirming.
                After gathering all details, present the information back to the customer for confirmation and allow changes if needed by including the keyword 'confirm' in your response.
                
                """
                messages = [{"role": "system", "content": instruction['show_flight']}]
                user_input = ""
        else:
            llm_output = conversation(user_input)
    
    elif status == 'show_flight' or status == 'exchange_show_flight':
        no_booking = ['no', 'nope', 'none']
        if user_input.lower() in no_booking: # user doesn't want to book, pure searching
            llm_output = "No problem! If you need assistance in the future or want to search for flights again, feel free to ask. Have a great day!"
            status = 'done'

        if user_input.lower() in confirm_keyword:
            llm_output = "Please press any key to continue..."
            user_info_book = json.loads(extract_information(messages[-1]['content'])) 
            user_info.update(user_info_book) # concat two dictionaries
            print("User information JSON updated")
            if status == 'exchange_show_flight':
                status = 'exchange_booking_after_confirmation'
            else:
                status = 'booking_after_confirmation'
        else:
            llm_output = conversation(user_input)
    
    if status == 'booking_after_confirmation':

        book_ticket = cli.book_ticket(user_info["user_id"], user_info["user_name"], user_info["passport_num"], user_info["flight_id"], user_info["num_passengers"], user_info["flight_class"], user_info["card_number"], user_info["expiry_date"], user_info["cvv"])
        if book_ticket:
            llm_output = f"Your ticket has been booked. Ticket ID: {book_ticket.order_id}. Thank you for using our service!"
        else:
            llm_output = "Your booking is not successful. Please try again."
        status = "done"
        
    if status == 'exchange_booking_after_confirmation':
        print(user_info)
        refund_result = cli.refund(user_info["user_id"], user_info["user_name"], user_info["passport_num"], order_id)
        if "Ticket refunded" in refund_result:
            new_ticket, price_gap = cli.exchange_ticket(order_id, user_info["passport_num"], user_info["user_id"], user_info["flight_id"], user_info["num_passengers"], user_info["card_number"], user_info["expiry_date"], user_info["cvv"])
            if new_ticket:
                llm_output = f"Your ticket has been exchanged. Price gap: {price_gap}. Thank you for using our service!"
            else:
                llm_output = "Your exchange is not successful. But your ticket has been refunded. Please try again."
        else:
            llm_output = refund_result
        status = "done"
    
    if status == 'refund':
        if user_input.lower() in confirm_keyword:
            llm_output = "Please press 'a' key to continue..."
            user_info.update(json.loads(extract_information(messages[-1]['content'])))
            refund_result = cli.refund(user_info["user_id"], user_info["user_name"], user_info["passport_num"], user_info["order_id"])
            
            llm_output = refund_result
            status = "done"
        else:
            llm_output = conversation(user_input)
            
    if status == 'exchange':
        if user_input.lower() in confirm_keyword:
            llm_output = "Please press 'a' key to continue....."
            user_info = json.loads(extract_information(messages[-1]['content']))

            order_id = user_info['order_id']
            print("order_id: ", order_id)
            status = 'exchange_search'
            user_input = ""
            messages = [{"role": "system", "content": instruction['search']}]

        else:
            llm_output = conversation(user_input)

    if status == 'done':
        llm_output += "\n\n The conversation has ended. You may now close the window. Thank you for using our service!"
        messages = [{"role": "system", "content": instruction['select']}]
        status = 'select'
        
    return llm_output   
        
            
def conversation(user_input):
    global messages
    if user_input:
        messages.append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            timeout=30,
            messages=messages,
        )
        
        content = response.choices[0].message.content
        messages.append({"role": "assistant", "content": content})
        
        return content

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
        If the information is not provided, do not add the key-value pair, neither the key.
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
        return content
    except Exception as e:
        print(e)
        time.sleep(0.5)
 
if __name__ == "__main__": # mock frontend
    while True:
        user_input = input("User: ")
        print("chatbot: ", interface(user_input))
    
