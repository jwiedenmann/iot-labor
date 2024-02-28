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
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    # insert_database()


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
    else:
        print("Disconnected from MQTT Broker.")


def connect_database():
    while (DB_CONNECTION is None):
        DB_CONNECTION = db.connect()
        time.sleep(5)

    db.check_and_create_table(DB_CONNECTION)


# def insert_database():
#     result = db.insert_into_table()
    
#     while(result == False):
#         connect_database()
#         result = db.insert_into_table()

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()