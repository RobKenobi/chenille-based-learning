import time
import paho.mqtt.client as mqtt

Connected = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the HiveMq broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")


broker = "broker.hivemq.com"
broker_port = 1883

name_robot = "chrysalide"
client = mqtt.Client(name_robot)

client.connect(broker, broker_port)

while True:
    client.publish(f"Chenille-based-learning/number_of_active_robots", 1)
    client.publish(f"Chenille-based-learning/{name_robot}/Leader", 1)
    time.sleep(1)
