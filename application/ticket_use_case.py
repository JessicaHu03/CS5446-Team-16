from domain.ticket import Ticket
from domain.flight import Flight
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
        if not flight or flight[8] < num_passengers: #flight[8] is stock, this code is temporary.
            return None
            # raise TicketNotAvailableException("Not enough tickets available for the selected flight.")
        
        total_price = flight[10] * num_passengers #flight[10] is price, this code is temporary.
        
        self.payment_gateway.process_payment(payment_info, total_price)
        self.flight_repository.update_flight_stock(flight_id, -num_passengers)
        order_id = self.order_repository.book_ticket(flight_id, user_id, 'Booked')
        
        ticket = Ticket(order_id, flight, user_id, num_passengers, total_price)

        return ticket

    def get_user_flight_id(self, order_id, passport_num, user_id):
        # is_correct = self.order_repository.is_order_correct(order_id, user_id, passport_num) # check user input
        # print("is_correct: ", is_correct)
        # if not is_correct:
        #     return None
            # raise OrderDoesNotExistException("Order does not exist or is not yours")
        return self.order_repository.get_flight_by_order(order_id)
    
    def exchange_ticket(self, order_id, flight_id, new_flight_id, user_id, num_passengers_to_change, payment_info):
        print(flight_id)
        flight_id = flight_id[0]
        print(flight_id)
        flight = self.flight_repository.get_flight_by_id(flight_id)
        new_flight = self.flight_repository.get_flight_by_id(new_flight_id)
        print("flight: ", flight)
        print("new_flight: ", new_flight)
        
        if not new_flight or new_flight[8] < num_passengers_to_change: #flight[8] is stock, this code is temporary.
            return("Not enough tickets available for the selected flight.")
            # raise TicketNotAvailableException("Not enough tickets available for the selected flight.")
        
        price_gap = (flight[10]-new_flight[10]) * num_passengers_to_change #flight[10] is price, this code is temporary.
        if price_gap > 0:
            self.payment_gateway.process_payment(payment_info, price_gap)
        if price_gap < 0:
            self.payment_gateway.process_payment(payment_info, -price_gap)
        
        self.flight_repository.update_flight_stock(new_flight_id, -num_passengers_to_change)
        self.flight_repository.update_flight_stock(flight_id, +num_passengers_to_change)
        order_id = self.order_repository.update_exchange_info(order_id, new_flight_id)

        new_ticket = Ticket(order_id, new_flight, user_id, num_passengers_to_change, price_gap) #flight[10] is price, this code is temporary.

        # print(f"Returning exchanged ticket: {new_ticket}, price_gap: {price_gap}")

        return new_ticket


    def refund_ticket(self, user_id, user_name,passport_num, order_id):
        try:
            flight_id = self.get_user_flight_id(order_id, passport_num, user_id)[0] #[0] is flight id, this code is temporary.
        except:
            return("Order does not exist or is not yours")
        
        is_refundable = self.flight_repository.is_flight_refundable(flight_id) # check if is refundable

        if is_refundable:
            # check status
            print(self.order_repository.check_order_status(order_id))
            if self.order_repository.check_order_status(order_id) == "Booked":
                self.order_repository.update_refund_info(order_id)
                self.flight_repository.update_flight_stock(flight_id, 1) # update flight stock
                refund_price = self.flight_repository.get_flight_by_id(flight_id)[-2] # get flight price
                self.payment_gateway.process_payment(refund_price, user_name) # mock refund
                
                return(f"Ticket refunded. Refund price: {refund_price}.")
            
            else: 
                return("Ticket status error. May not be refundable or has been exchanged/refunded.")
        else:
            return("Ticket unrefundable")

        
