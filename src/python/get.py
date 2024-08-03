import mysql.connector
import json

def get_them(): 
    conn = mysql.connector.connect(user='wiedenmann', password='Bcdrf6.x',host='localhost',database='wiedenmann')
    cursor = conn.cursor()

    query = f"""
    select 
        id
        ,millis
        ,accX
        ,accY
        ,accZ
        ,gyrX
        ,gyrY
        ,gyrZ
        ,magX
        ,magY
        ,magZ
        ,temp
        ,insert_time
    from acceleration
    order by insert_time asc"""

    cursor.execute(query)

    print("id;millis;accX;accY;accZ;gyrX;gyrY;gyrZ;magX;magY;magZ;temp;insert_time")

    for id, millis, accX, accY, accZ, gyrX, gyrY, gyrZ, magX, magY, magZ, temp, insert_time in cursor:
        print(id, ";", millis, ";", accX, ";", accY, ";", accZ, ";", gyrX, ";", gyrY, ";", gyrZ, ";", magX, ";", magY, ";", magZ, ";", temp, ";", insert_time)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    get_them()

# python3 get.py > get.csv
# scp wiedenmann@164.92.190.0:get.csv /mnt/c/Users/jwiedenmann/Downloads