import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="network_devices"
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
