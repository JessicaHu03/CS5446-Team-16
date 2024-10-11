from domain.ticket import Ticket
from domain.exceptions import TicketNotAvailableException, OrderDoesNotExistException, FlightNotRefundableException

class TicketUseCase:
    def __init__(self, flight_repository, payment_gateway, order_repository):
        self.flight_repository = flight_repository
        self.payment_gateway = payment_gateway
        self.order_repository = order_repository
        
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

    def refund_ticket(self, user_id, user_name,passport_num, order_id):
        is_correct = self.order_repository.is_order_correct(order_id, user_id, passport_num) # check user input
        if not is_correct:
            raise OrderDoesNotExistException("Order does not exist or is not yours")
        flight_id = self.order_repository.get_flight_by_order(order_id)
        is_refundable = self.flight_repository.is_flight_refundable(flight_id) # check if is refundable
        if is_refundable:
            self.flight_repository.update_flight_stock(flight_id, 1) # update flight stock
            refund_price = self.flight_repository.get_flight_by_id(flight_id)[-2] # get flight price
            self.payment_gateway.process_payment(refund_price, user_name) # mock refund
            
            return True
        else:
            raise FlightNotRefundableException("Flight cannot be refunded")
        