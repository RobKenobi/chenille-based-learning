import time
import paho.mqtt.client as mqtt
import threading
import numpy as np

Connected = False

radius = np.zeros((2, 1))
names = ["Robot1", "Robot2"]

sem = threading.Semaphore()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
        client.publish("Chenille-based-learning/Server/population", 0, qos=2, retain=True)
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    data = message.payload.decode()
    topic_name = message.topic
    if topic_name[31:-11] == "Robot1":
        radius[0] = data
    if topic_name[31:-11] == "Robot2":
        radius[1] = data


def check_population(client, userdata, message):
    print("Current population:", str(message.payload.decode()))


def on_disconnect(client, userdata, rc):
    print("Disconnected to the broker")


broker = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("Server", clean_session=False)

client.on_connect = on_connect

client.message_callback_add("Chenille-based-learning/Server/population", check_population)
client.message_callback_add("Chenille-based-learning/Robots/+/BallRadius", on_message)

client.on_disconnect = on_disconnect

client.connect(broker, broker_port, keepalive=60)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    time.sleep(1)

client.subscribe("Chenille-based-learning/Robots/#")

try:
    while True:
        followers = names.copy()
        leader = followers[np.argmax(radius)]
        followers.remove(leader)
        print(radius)
        if np.max(radius) != 0:

            print("Le leader est ", leader)

            client.publish(f"Chenille-based-learning/Robots/{leader}/status", 1, qos=1, retain=True)
            for follower in followers:
                client.publish(f"Chenille-based-learning/Robots/{follower}/status", 0, qos=1, retain=True)

        time.sleep(1)

except KeyboardInterrupt:
    for name in names:
        client.publish(f"Chenille-based-learning/Robots/{name}/status", -1, qos=1)
    client.disconnect()
    client.loop_stop()
