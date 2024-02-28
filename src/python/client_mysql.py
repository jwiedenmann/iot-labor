import paho.mqtt.client as mqtt
import mysql.connector

# create table sensordata(id integer NOT NULL AUTO_INCREMENT PRIMARY KEY,ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, topic varchar(100), msg varchar(1000));

# The callback function of connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("/dhai/Heidenheim/till.haenisch@dhbw-heidenheim.de/#")

# The callback function for received message
def on_message(client, userdata, msg):
    global cursor
    print(msg.topic+" "+msg.payload.decode("utf-8"))
    sql = "INSERT INTO sensordata(topic,msg) values('" + msg.topic + "','" + msg.payload.decode("utf-8") + "')"
    print(sql)
    res = cursor.execute(sql)
    conn.commit();
    print(res)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="haenisch",password="geheim")
while (True):
	try:
		client.connect("ai.tillh.de", 1883, 60)

		conn = mysql.connector.connect(user='tiill', password='geheim',
                              host='localhost',
                              database='iot')
		cursor = conn.cursor()

		client.loop_forever()
		conn.close()
	except Exception as error:
	   print(error)
