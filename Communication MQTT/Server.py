import threading
import time

import numpy as np
import paho.mqtt.client as mqtt

Connected = False

radius = np.zeros((2, 1))
names = ["Robot1", "Robot2"]

sem = threading.Semaphore()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")


def on_radius(client, userdata, message):
    data = message.payload.decode()
    topic_name = message.topic
    if topic_name.split('/')[2] == "Robot1":
        radius[0] = data
    if topic_name.split('/')[2] == "Robot2":
        radius[1] = data


def on_disconnect(client, userdata, rc):
    print("Disconnected to the broker")


broker = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("Server", clean_session=False)

client.on_connect = on_connect

client.message_callback_add("Chenille-based-learning/Robots/+/BallRadius", on_radius)

client.on_disconnect = on_disconnect

client.connect(broker, broker_port, keepalive=60)

client.loop_start()  # Start the loop

while not Connected:  # Wait for the client to connect
    time.sleep(1)

client.subscribe("Chenille-based-learning/Robots/#")

last_publish = time.time()
try:
    while True:
        followers = names.copy()
        leader = followers[np.argmax(radius)]
        followers.remove(leader)

        if time.time() - last_publish > 0.5:
            if np.max(radius) != 0:
                print("Le leader est ", leader)
                client.publish(f"Chenille-based-learning/Robots/{leader}/status", 1, qos=1, retain=True)

                for follower in followers:
                    client.publish(f"Chenille-based-learning/Robots/{follower}/status", 0, qos=1, retain=True)
            else:
                print("Aucun robot ne voit la balle")
                for robot in names:
                    client.publish(f"Chenille-based-learning/Robots/{robot}/status", -1, qos=1, retain=True)
            last_publish = time.time()

except KeyboardInterrupt:
    print("Arrêt de tous les robots")
    for name in names:
        client.publish(f"Chenille-based-learning/Robots/{name}/status", -1, qos=1)
    client.disconnect()
    client.loop_stop()
