import time
import paho.mqtt.client as mqtt
import acceleration_mysql as db

# MQTT Broker settings
MQTT_BROKER = "ai.tillh.de" 
MQTT_PORT = 1883
MQTT_TOPIC = "/dhai/Heidenheim/wiedenmannj.tin21@student.dhbw-heidenheim.de/#"

DB_CONNECTION = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
        connect_database()
    else:
        print(f"Failed to connect, return code {rc}\n")


def on_message(client, userdata, msg):
    jsondata = msg.payload.decode()
    print(f"Received `{jsondata}` from `{msg.topic}` topic")
    insert_database(jsondata)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
    else:
        print("Disconnected from MQTT Broker.")


def connect_database():
    DB_CONNECTION = db.connect()

    while (DB_CONNECTION is None):
        DB_CONNECTION = db.connect()
        time.sleep(5)

    db.check_and_create_table(DB_CONNECTION)


def insert_database(jsondata):
    result = db.insert_into_table()
    
    while(result == False):
        connect_database()
        result = db.insert_into_table(DB_CONNECTION, jsondata)

def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.username_pw_set(username="wiedenmann",password="Bcdrf6.x")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()