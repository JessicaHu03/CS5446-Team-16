from application.ticket_use_case import TicketUseCase
from infrastructure.flight_repository import FlightRepository
from infrastructure.payment_gateway import PaymentGateway

# Instantiate dependencies
flight_repo = FlightRepository(db_connection="data/airline.db")
payment_gateway = PaymentGateway()
ticket_use_case = TicketUseCase(flight_repo, payment_gateway)

def available_tickets():
    departure = input("Enter departure city: ")
    destination = input("Enter destination city: ")
    date = input("Enter departure date (YYYY-MM-DD): ")
    flight_class = input("Enter flight class (Economy/Business): ")
    num_passengers = int(input("Enter number of passengers: "))
    
    available_flights = ticket_use_case.search_available_flights(departure, destination, date, flight_class, num_passengers)


    print("Available flights:")
    for flight in available_flights:
        print(flight)

def book_ticket():
    flight_id = int(input("Enter flight ID to book: "))
    user_id = int(input("Enter user ID: "))
    user_name = input("Enter your name: ")
    passport_num = input("Enter your passport number: ")
    num_passengers = int(input("Enter number of passengers: "))
    payment_info = {
        'card_number': input("Enter card number: "),
        'expiry_date': input("Enter card expiry date (MM/YY): "),
        'cvv': input("Enter CVV: ")
    }
    
    connection = flight_repo.connect()
    cursor = connection.cursor()
    cursor.execute('INSERT OR IGNORE INTO User (id, name, passport_num) VALUES (?, ?, ?)', (user_id, user_name, passport_num))
    connection.commit()
    connection.close()
    
    ticket = ticket_use_case.book_ticket(flight_id, user_id, num_passengers, payment_info)
    print("Ticket booked:", ticket)