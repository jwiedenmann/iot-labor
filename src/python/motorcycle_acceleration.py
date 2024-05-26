import json
import re
import paho.mqtt.client as mqtt
import acceleration_mysql as db

# MQTT Broker settings
MQTT_BROKER = "ai.tillh.de" 
MQTT_PORT = 1883
MQTT_TOPIC = "/dhai/Heidenheim/wiedenmannj.tin21@student.dhbw-heidenheim.de/#"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
        connect_database()
    else:
        print(f"Failed to connect, return code {rc}\n")


def on_message(client, userdata, msg):
    jsondata = msg.payload.decode()
    data = None

    print(f"Received `{jsondata}` from `{msg.topic}` topic")

    try:
        # Try to load JSON to handle invalid NaN or Infinity values
        data = json.loads(jsondata)
    except json.JSONDecodeError:
        # Replace 'NaN' with None (which becomes 'null' in JSON)
        cleaned_jsondata = re.sub(r'\b[nN][aA][nN]\b', '0', jsondata)
        print(f"Cleaned json data: `{jsondata}`")

        data = json.loads(cleaned_jsondata)  # Re-parse the cleaned JSON

    insert_database(data)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")
    else:
        print("Disconnected from MQTT Broker.")


def connect_database():
    connection = db.connect()
    db.check_and_create_table(connection)
    connection.close()


def insert_database(jsondata):
    connection = db.connect()
    result = db.insert_into_table(connection, jsondata)

    while(result == False):
        connection = db.connect()
        result = db.insert_into_table(connection, jsondata)

def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.username_pw_set(username="wiedenmann",password="Bcdrf6.x")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()