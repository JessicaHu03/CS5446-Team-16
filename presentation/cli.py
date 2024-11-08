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

    available_flights = ticket_use_case.search_available_flights(
        departure, destination, date, flight_class, num_passengers)
    flight = []
    # print("Available flights:")
    # for flight in available_flights:
    #     print(flight)
    
    return available_flights

def book_ticket(user_id, user_name, passport_num, flight_id, num_passengers, flight_class, card_number, expiry_date, cvv):
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

    return ticket


def refund(user_id, user_name, passport_num, order_id):
    # user_id = int(input("Enter user ID: "))
    # user_name = input("Enter your name: ")
    # passport_num = input("Enter your passport number: ")
    # order_id = int(input("Enter order ID: "))

    result = ticket_use_case.refund_ticket(
        user_id, user_name, passport_num, order_id)
    return result

def check_order(order_id, passport_num, user_id):
    
    flight_id=ticket_use_case.get_user_flight_id(order_id, passport_num, user_id)
    if flight_id is None:
        return False
    return True

def exchange_ticket(order_id, passport_num, user_id, new_flight_id, num_passengers_to_change, card_number, expiry_date, cvv):
    print(order_id)
    flight_id = ticket_use_case.get_user_flight_id(order_id, passport_num, user_id)
    print(flight_id)
    payment_info = {
        'card_number': card_number,
        'expiry_date': expiry_date,
        'cvv': cvv
    }

    new_ticket = ticket_use_case.exchange_ticket(order_id, flight_id, new_flight_id, user_id, num_passengers_to_change, payment_info)
    price_gap = new_ticket.total_price
    print("Ticket exchanged successfully:", new_ticket)
    
    return new_ticket, price_gap