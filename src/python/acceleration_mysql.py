import time
import mysql.connector
from mysql.connector import Error

DATABASE = 'wiedenmann'
USER = 'wiedenmann'
PASSWORD = 'Bcdrf6.x'
TABLE_NAME = 'acceleration'

def connect():
    connection = None

    while (connection is None):
        try:
            connection = mysql.connector.connect(
                database=DATABASE,
                user=USER,
                password=PASSWORD
            )

            return connection
        
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

        time.sleep(5)

def check_and_create_table(connection):
    """Check if a table exists and create it if not."""
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{TABLE_NAME}';")
    result = cursor.fetchone()
    if result:
        print(f"Table {TABLE_NAME} already exists.")
    else:
        create_table_query = f"""
        CREATE TABLE {TABLE_NAME} (
            id      INT     AUTO_INCREMENT PRIMARY KEY,
            millis  BIGINT  UNSIGNED    NOT NULL,
            accX    FLOAT   NOT NULL,
            accY    FLOAT   NOT NULL,
            accZ    FLOAT   NOT NULL,
            gyrX    FLOAT   NOT NULL,
            gyrY    FLOAT   NOT NULL,
            gyrZ    FLOAT   NOT NULL,
            magX    FLOAT   NOT NULL,
            magY    FLOAT   NOT NULL,
            magZ    FLOAT   NOT NULL,
            temp    FLOAT   NOT NULL,
            insert_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            cursor.execute(create_table_query)
            print(f"Table {TABLE_NAME} created successfully.")
        except Error as e:
            print(f"Failed to create table {TABLE_NAME}: {e}")

def insert_into_table(connection, jsonData):
    cursor = connection.cursor()
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (millis, accX, accY, accZ, gyrX, gyrY, gyrZ, magX, magY, magZ, temp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(
            insert_query,
            (
                jsonData['millis'], 
                jsonData['accX'], jsonData['accY'], jsonData['accZ'], 
                jsonData['gyrX'], jsonData['gyrY'], jsonData['gyrZ'], 
                jsonData['magX'], jsonData['magY'], jsonData['magZ'],
                jsonData['temp']
            ))
        connection.commit()
        print(f"Record inserted successfully into {TABLE_NAME} table.")
        return True
    except Error as e:
        print(f"Failed to insert into table {TABLE_NAME}: {e}")
        return False