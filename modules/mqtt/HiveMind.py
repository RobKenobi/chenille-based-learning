import time
import paho.mqtt.client as mqtt
import json
import threading
import numpy as np

Connected = False

radius = np.zeros((2, 1))
names = ["Chenille", "Chrysalide"]

sem = threading.Semaphore()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
        client.publish("Chenille-based-learning/HiveMind/population", 0, qos=2, retain=True)
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    # data = json.loads(message.payload)
    data = message.payload.decode()
    topic_name = message.topic
    if topic_name[30:-7] == "Chenille":
        radius[0] = data
    if topic_name[30:-7] == "Chrysalide":
        radius[1] = data


def check_population(client, userdata, message):
    print("Current population:", str(message.payload.decode()))


def on_disconnect(client, userdata, rc):
    print("Disconnected to the broker")


broker = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("HiveMind", clean_session=False)

client.on_connect = on_connect

client.message_callback_add("Chenille-based-learning/HiveMind/population", check_population)
client.message_callback_add("Chenille-based-learning/Swarm/+/Target", on_message)

client.on_disconnect = on_disconnect

client.connect(broker, broker_port, keepalive=60)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    time.sleep(1)

client.subscribe("Chenille-based-learning/Swarm/#")

try:
    while True:
        followers = names.copy()
        leader = followers[np.argmax(radius)]

        followers.remove(leader)

        if np.max(radius) != 0:
            print("Le leader est ", leader)
            client.publish(f"Chenille-based-learning/Swarm/{leader}/status", 1, qos=1)
            for follower in followers:
                client.publish(f"Chenille-based-learning/Swarm/{follower}/status", 0, qos=1)
        # if leader == names[1]:  # If chrysalide is leader

        time.sleep(1)

except KeyboardInterrupt:
    for name in names:
        client.publish(f"Chenille-based-learning/Swarm/{name}/status", -1, qos=1)
    client.disconnect()
    client.loop_stop()
