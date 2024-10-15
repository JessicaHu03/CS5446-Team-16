# infrastructure/flight_repository.py
import sqlite3

class FlightRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def connect(self):
        # Connect to the SQLite database
        return sqlite3.connect(self.db_connection)

    def search_flights(self, departure, destination, date, flight_class):
        connection = self.connect()
        cursor = connection.cursor()
        query = '''
        SELECT * FROM Flight 
        WHERE LOWER(departure) = LOWER(?) AND LOWER(destination) = LOWER(?) AND departure_time LIKE ? AND LOWER(class) = LOWER(?) AND stock > 0
        '''
        date_pattern = date + '%'
        print(f"Executing query with: departure={departure}, destination={destination}, date_pattern={date_pattern}, flight_class={flight_class}")
        cursor.execute(query, (departure, destination, date_pattern, flight_class))
        flights = cursor.fetchall()
        connection.close()
        print(f"Flights found: {flights}")
        return flights



    def get_flight_by_id(self, flight_id):
        connection = self.connect()
        cursor = connection.cursor()
        query = 'SELECT * FROM Flight WHERE id = ?'
        cursor.execute(query, (flight_id,))
        flight = cursor.fetchone()
        connection.close()
        return flight

    def update_flight_stock(self, flight_id, num_passengers_change):
        connection = self.connect()
        cursor = connection.cursor()
        query = 'UPDATE Flight SET stock = stock + ? WHERE id = ?'
        cursor.execute(query, (num_passengers_change, flight_id))
        connection.commit()
        connection.close()

    def is_flight_refundable(self, flight_id):
        connection = self.connect()
        cursor = connection.cursor()
        query = 'SELECT is_refundable FROM Flight WHERE id = ?'
        cursor.execute(query, (flight_id))
        is_refundable = cursor.fetchone()[0]
        return is_refundable