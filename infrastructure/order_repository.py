import sqlite3

class OrderRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def connect(self):
        # Connect to the SQLite database
        return sqlite3.connect(self.db_connection)
    
    def is_order_correct(self, order_id, user_id, passport_num):
        connection = self.connect()
        cursor = connection.cursor()
        query = 'SELECT * FROM Order WHERE id = ? AND user_id = ?'
        cursor.execute(query, (order_id, user_id, passport_num))
        order = cursor.fetchone()
        connection.close()
        
        query = 'SELECT * FROM User WHERE id = ? AND passport_num = ?'
        cursor.execute(query, (user_id, passport_num))
        user = cursor.fetchone()
        connection.close()
        
        return order is not None and user is not None
    
    def get_flight_by_order(self, order_id):
        connection = self.connect()
        cursor = connection.cursor()
        query = 'SELECT flight_id FROM Order WHERE id = ?'
        cursor.execute(query, (order_id))
        flight_id = cursor.fetchone()
        connection.close()
        return flight_id