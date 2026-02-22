import os
from datetime import datetime
import mysql.connector

"""
    Connects to MariaDB (running in Docker).
    Environment variables come from docker-compose.yml.
"""
def get_db_connection():
   
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "3307")),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "password"),
        database=os.environ.get("DB_NAME", "traveldb"),
    )

"""
    Tables are created by db/init.sql automatically.
"""
def init_db():
    return


"""
    Returns a MariaDB-friendly timestamp string.
"""
def now_iso() -> str:
 
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")