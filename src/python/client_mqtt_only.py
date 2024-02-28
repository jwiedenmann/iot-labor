import paho.mqtt.client as mqtt

# The callback function of connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/dhai/Heidenheim/till.haenisch@dhbw-heidenheim.de/#")

# The callback function for received message
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username="wiedenmann",password="Bcdrf6.x")
    client.connect("ai.tillh.de", 1883, 60)

    client.loop_forever()
except:
  print("An exception occurred")
