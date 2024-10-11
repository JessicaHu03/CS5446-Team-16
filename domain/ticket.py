class Ticket:
    def __init__(self, flight, user_id, num_passengers, total_price, status='Booked'):
        self.flight = flight
        self.user_id = user_id
        self.num_passengers = num_passengers
        self.total_price = total_price
        self.status = status

    def __repr__(self):
        return f"Ticket(flight_num={self.flight[1]}, departure={self.flight[2]}, destination={self.flight[3]}, departure_time={self.flight[4]}, user_id={self.user_id}, num_passengers={self.num_passengers}, total_price={self.total_price})"
        self.flight = flight
        self.user_id = user_id
        self.num_passengers = num_passengers
        self.total_price = total_price
        self.status = status