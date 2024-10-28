import sqlite3

class OrderRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def connect(self):
        # Connect to the SQLite database
        return sqlite3.connect(self.db_connection)
    
    def book_ticket(self, flight_id, user_id, status):
        connection = self.connect()
        cursor = connection.cursor()
        
        query = 'INSERT INTO "orders" (flight_id, user_id, status) VALUES (?, ?, ?)'
        cursor.execute(query, (flight_id, user_id, status))
        
        connection.commit()
        connection.close()
        
        return cursor.lastrowid

    def is_order_correct(self, order_id, user_id, passport_num):
        connection = self.connect()
        cursor = connection.cursor()
        query = 'SELECT * FROM "orders" WHERE id = ? AND user_id = ?'
        cursor.execute(query, (order_id, user_id))
        order = cursor.fetchone()
        
        query = 'SELECT * FROM "User" WHERE id = ? AND passport_num = ?'
        cursor.execute(query, (user_id, passport_num))
        user = cursor.fetchone()
        connection.close()
        
        return order is not None and user is not None
    
    def get_flight_by_order(self, order_id):
        connection = self.connect()
        cursor = connection.cursor()
        query = 'SELECT flight_id FROM "orders" WHERE id = ?'
        cursor.execute(query, (order_id,))
        flight_id = cursor.fetchone()
        connection.close()
        return flight_id
    
    def check_order_status(self, flight_id):
        connection = self.connect()
        cursor = connection.cursor()
        
        query = 'SELECT status FROM "orders" WHERE flight_id = ?'
        cursor.execute(query, (flight_id,))
        
        status = cursor.fetchone()
        connection.close()
        
        return status[0] if status else None
    
    def update_refund_info(self, flight_id):
        connection = self.connect()
        cursor = connection.cursor()
        
        query = 'UPDATE "orders" SET status = ? WHERE flight_id = ?'
        cursor.execute(query, ("Refunded", flight_id))
        
        connection.commit()
        connection.close()

    def update_exchange_info(self, order_id, new_flight_id):
        connection = self.connect()
        cursor = connection.cursor()
        
        query = 'UPDATE "orders" SET status = ?, flight_id = ? WHERE id = ?'
        cursor.execute(query, ("Exchanged", new_flight_id, order_id))
        
        connection.commit()
        connection.close()

