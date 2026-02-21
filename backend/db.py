import os
import sqlite3
from datetime import datetime



# Finds the path to the database file
DB_Path = os.path.join(os.path.dirname(__file__), "travel.db")


# Creates and returns a connection to the database
def get_db_connection():
    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row
    return conn


"""

Initializes the database by creating the necessary tables if they do not exist.

we run it when we start so the project can start "fresh" without manually creating the database and tables.
"""
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()


    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the destinations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_from TEXT NOT NULL,
            date_to TEXT NOT NULL,
            description TEXT,
            location TEXT,
            country TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


    # Helper function to get the current timestamp in ISO string format "2024-06-01T12:34:56.789123"
    def now_iso():
        return datetime.now().isoformat()