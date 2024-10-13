from domain.ticket import Ticket
from domain.exceptions import TicketNotAvailableException

class TicketUseCase:
    def __init__(self, flight_repository, payment_gateway):
        self.flight_repository = flight_repository
        self.payment_gateway = payment_gateway

    def search_available_flights(self, departure, destination, date, flight_class, num_passengers):
        flights = self.flight_repository.search_flights(departure, destination, date, flight_class)

        return flights

    def book_ticket(self, flight_id, user_id, num_passengers, payment_info):
        flight = self.flight_repository.get_flight_by_id(flight_id)
        if not flight or flight.stock < num_passengers:
            raise TicketNotAvailableException("Not enough tickets available for the selected flight.")
        
        total_price = flight.price * num_passengers
        self.payment_gateway.process_payment(payment_info, total_price)
        
        ticket = Ticket(flight, user_id, num_passengers, total_price)
        self.flight_repository.update_flight_stock(flight_id, -num_passengers)
        return ticket

    def exchange_ticket(self, ticket):
        new_ticket = ticket
        return new_ticket
    
    def refund(self, ticket):
        return ticket