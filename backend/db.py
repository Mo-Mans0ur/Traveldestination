import os
import time
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


"""Return current time as Unix epoch seconds (int).

This matches the BIGINT created_at/updated_at columns in init.sql.
"""
def now_epoch() -> int:

    return int(time.time())