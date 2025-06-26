import sqlite3
from datetime import datetime, timedelta

def create_database():
    try:
        conn = sqlite3.connect("coffee_shop.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                date_added TEXT NOT NULL,
                shelf_life INTEGER,
                expiration_date TEXT,
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating database or tables: {e}")
    finally:
        if conn:
            conn.close()


def add_stock(user_id, stock_name, quantity, quantity_unit, shelf_life, date_added):
    try:
        conn = sqlite3.connect('coffee_shop.db')
        cursor = conn.cursor()

        expiration_date = (datetime.now() + timedelta(days=shelf_life)).strftime('%Y-%m-%d') if shelf_life is not None else None

        cursor.execute(''' 
            INSERT INTO stocks (user_id, name, quantity, unit, date_added, shelf_life, expiration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, stock_name, quantity, quantity_unit, date_added, shelf_life, expiration_date))

        conn.commit()
        print(f"Stock '{stock_name}' added successfully!")

    except sqlite3.Error as e:
        print(f"Error adding stock: {e}")
    finally:
        if conn:
            conn.close()

def update_stock(stock_id, name, quantity, unit, shelf_life, date_added):
    try:
        conn = sqlite3.connect('coffee_shop.db')
        cursor = conn.cursor()

        if shelf_life is not None:
            expiration_date = (datetime.strptime(date_added, '%Y-%m-%d') + timedelta(days=shelf_life)).strftime('%Y-%m-%d')
        else:
            expiration_date = None

        cursor.execute('''
        UPDATE stocks
        SET name = ?, quantity = ?, unit = ?, date_added = ?, shelf_life = ?, expiration_date = ?
        WHERE stock_id = ?
        ''', (name, quantity, unit, date_added, shelf_life, expiration_date, stock_id))

        conn.commit()
        print(f"Stock ID {stock_id} updated successfully!")
    except sqlite3.Error as e:
        print(f"Error updating stock: {e}")
    finally:
        if conn:
            conn.close()


def delete_stock(stock_id):
    try:
        conn = sqlite3.connect('coffee_shop.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stocks WHERE stock_id = ?", (stock_id,))
        conn.commit()
        print(f"Stock ID {stock_id} deleted successfully!")
    except sqlite3.Error as e:
        print(f"Error deleting stock: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def get_all_stocks():
    try:
        conn = sqlite3.connect('coffee_shop.db')
        cursor = conn.cursor()
        cursor.execute('SELECT stock_id, name, quantity, unit, date_added, shelf_life, expiration_date FROM stocks')
        stocks = cursor.fetchall()
        return stocks
    except sqlite3.Error as e:
        print(f"Error fetching all stocks: {e}")
        return []
    finally:
        if conn:
            conn.close()

