from application.ticket_use_case import TicketUseCase
from infrastructure.flight_repository import FlightRepository
from infrastructure.payment_gateway import PaymentGateway
from infrastructure.order_repository import OrderRepository

# Instantiate dependencies
flight_repo = FlightRepository(db_connection="data/airline.db")
order_repo = OrderRepository(db_connection="data/airline.db")
payment_gateway = PaymentGateway()
ticket_use_case = TicketUseCase(flight_repo, payment_gateway, order_repo)


def available_tickets(departure, destination, date, flight_class, num_passengers):
    # departure = input("Enter departure city: ")
    # destination = input("Enter destination city: ")
    # date = input("Enter departure date (YYYY-MM-DD): ")
    # flight_class = input("Enter flight class (Economy/Business): ")
    # num_passengers = int(input("Enter number of passengers: "))

    available_flights = ticket_use_case.search_available_flights(
        departure, destination, date, flight_class, num_passengers)

    print("Available flights:")
    for flight in available_flights:
        print(flight)


def book_ticket(user_id, user_name, passport_num, flight_id, num_passengers, card_number, expiry_date, cvv):
    # flight_id = int(input("Enter flight ID to book: "))
    # user_id = int(input("Enter user ID: "))
    # user_name = input("Enter your name: ")
    # passport_num = input("Enter your passport number: ")
    # num_passengers = int(input("Enter number of passengers: "))
    # payment_info = {
    #     'card_number': input("Enter card number: "),
    #     'expiry_date': input("Enter card expiry date (MM/YY): "),
    #     'cvv': input("Enter CVV: ")
    # }
    payment_info = {
        'card_number': card_number,
        'expiry_date': expiry_date,
        'cvv': cvv
    }

    connection = flight_repo.connect()
    cursor = connection.cursor()
    cursor.execute('INSERT OR IGNORE INTO User (id, name, passport_num) VALUES (?, ?, ?)',
                   (user_id, user_name, passport_num))
    connection.commit()
    connection.close()

    ticket = ticket_use_case.book_ticket(
        flight_id, user_id, num_passengers, payment_info)
    print("Ticket booked:", ticket)


def refund(user_id, user_name, passport_num, order_id):
    # user_id = int(input("Enter user ID: "))
    # user_name = input("Enter your name: ")
    # passport_num = input("Enter your passport number: ")
    # order_id = int(input("Enter order ID: "))

    result = ticket_use_case.refund_ticket(
        user_id, user_name, passport_num, order_id)
    if result:
        print("Ticket refunded.")
    else:
        print("Ticket not refunded due to error.")

def check_order(order_id, passport_num, user_id):
    
    flight_id=ticket_use_case.get_user_flight_id(order_id, passport_num, user_id)

    return True

def exchange_ticket(order_id, passport_num, user_id, departure, destination, date, flight_class, num_passengers_to_change, card_number, expiry_date, cvv):
    # user_id = int(input("Enter user ID: "))
    # order_id = input("Enter your order ID: ")
    # passport_num = int(input("Enter Passport: "))

    flight_id=ticket_use_case.get_user_flight_id(order_id, passport_num, user_id)
    
    # departure = input("Enter departure city: ")
    # destination = input("Enter destination city: ")
    # date = input("Enter departure date (YYYY-MM-DD): ")
    # flight_class = input("Enter flight class (Economy/Business): ")
    # num_passengers_to_change = int(input("Enter number of passengers to exchange: "))

    new_flight_id = ticket_use_case.search_available_flights(departure, destination, date, flight_class, num_passengers_to_change)
    
    # payment_info = {
    #     'card_number': input("Enter card number: "),
    #     'expiry_date': input("Enter card expiry date (MM/YY): "),
    #     'cvv': input("Enter CVV: ")
    # }

    payment_info = {
        'card_number': card_number,
        'expiry_date': expiry_date,
        'cvv': cvv
    }

    try:
        new_ticket = ticket_use_case.exchange_ticket(
            flight_id, new_flight_id, user_id, num_passengers_to_change, payment_info
        )
        print("Ticket exchanged successfully:", new_ticket)

    except Exception as e:
        print(f"Error: {e}")