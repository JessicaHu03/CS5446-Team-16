class Flight:
    def __init__(self, flight_num, departure, destination, departure_time, arrival_time, duration, flight_class, price, is_refundable):
        self.flight_num = flight_num
        self.departure = departure
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.flight_class = flight_class
        self.price = price
        self.is_refundable = is_refundable