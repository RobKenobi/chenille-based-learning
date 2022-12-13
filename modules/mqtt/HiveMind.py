import time
import paho.mqtt.client as mqtt
import json
import threading
import numpy as np

Connected = False
leader = 0
list_radius = np.array([])
radius = np.zeros((2, 1))
radius_dict = {}

sem = threading.Semaphore()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
        client.publish("Chenille-based-learning/HiveMind/population", 0, qos=2, retain=True)
        client.publish("Chenille-based-learning/HiveMind/leader", leader, qos=1, retain=True)
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    data = json.loads(message.payload)
    print(data)
    print(message.topic)
    global radius_dict
    # global radius
    radius_dict[data["Name"]] = data["Target"]

    # if data["Name"] == "Chenille":
    #     radius[0] = data["Target"]
    # if data["Name"] == "Chrysalide":
    #     radius[1] = data["Target"]


# print("message retain flag=", message.retain)


def check_population(client, userdata, message):
    print("Current population:", str(message.payload.decode()))


# def get_radius(client, userdata, message):
# global list_radius
# list_radius = np.append(list_radius, float(message.payload.decode()))


def on_disconnect(client, userdata, rc):
    print("Disconnected to the broker")


broker = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("HiveMind", clean_session=False)

client.on_connect = on_connect

# client.message_callback_add()
client.message_callback_add("Chenille-based-learning/HiveMind/population", check_population)
client.message_callback_add("Chenille-based-learning/Swarm/#", on_message)
# client.message_callback_add("Chenille-based-learning/Swarm/#", get_radius)
# client.on_message = on_message
# client.on_publish = on_publish
client.on_disconnect = on_disconnect

client.connect(broker, broker_port, keepalive=60)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    time.sleep(1)

client.subscribe("Chenille-based-learning/Swarm/#")

try:
    while True:
        print(radius_dict)
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
