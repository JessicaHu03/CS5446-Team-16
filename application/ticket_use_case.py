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

    def exchange_ticket(self, flight_id, new_flight_id, user_id, num_passengers_to_change, payment_info):
        flight = self.flight_repository.get_flight_by_id(flight_id)
        new_flight = self.flight_repository.get_flight_by_id(new_flight_id)
        
        if not new_flight_id or new_flight_id.stock < num_passengers_to_change:
            raise TicketNotAvailableException("Not enough tickets available for the selected flight.")
        
        price_gap = (flight.price-new_flight.price) * num_passengers_to_change
        if price_gap > 0:
            self.payment_gateway.process_payment(payment_info, price_gap)
        if price_gap < 0:
            self.payment_gateway.process_payment(payment_info, -price_gap)
        
        new_ticket = Ticket(new_flight, user_id, num_passengers_to_change, new_flight.price)
        self.flight_repository.update_flight_stock(new_flight, -num_passengers_to_change)
        self.flight_repository.update_flight_stock(flight, +num_passengers_to_change)
        
        return new_ticket
    
    