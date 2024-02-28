import mysql.connector
from mysql.connector import Error

DATABASE = 'wiedenmann'
USER = 'wiedenmann'
PASSWORD = 'Bcdrf6.x'
TABLE_NAME = 'acceleration'

def connect():
    try:
        connection = mysql.connector.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

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
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            info TEXT
        );
        """
        try:
            cursor.execute(create_table_query)
            print(f"Table {TABLE_NAME} created successfully.")
        except Error as e:
            print(f"Failed to create table {TABLE_NAME}: {e}")

def insert_into_table(connection, name, info):
    """Insert a row into the table."""
    cursor = connection.cursor()
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (name, info)
    VALUES (%s, %s);
    """
    try:
        cursor.execute(insert_query, (name, info))
        connection.commit()
        print(f"Record inserted successfully into {TABLE_NAME} table.")
        return True
    except Error as e:
        print(f"Failed to insert into table {TABLE_NAME}: {e}")
        return False