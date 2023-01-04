import random
import time

import paho.mqtt.client as mqtt

Connected = False

i = None

status = -1


def update_population(client, userdata, message):
    global i
    i = int(message.payload.decode())


def get_status(client, userdata, message):
    global status
    status = int(message.payload.decode())


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
        client.subscribe("Chenille-based-learning/Server/population")
        client.subscribe("Chenille-based-learning/Robots/#")
    else:
        print("Connection failed")


broker = "broker.hivemq.com"
broker_port = 1883

name_robot = "Robot2"
client = mqtt.Client(name_robot, clean_session=True)

# Callbacks
client.on_connect = on_connect

client.message_callback_add("Chenille-based-learning/Server/population", update_population)
client.message_callback_add(f"Chenille-based-learning/Robots/{name_robot}/status", get_status)

client.connect(broker, broker_port, keepalive=10)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    time.sleep(1)

client.publish("Chenille-based-learning/Server/population", i + 1, qos=2, retain=True)
# -1: waiting for instructions from the server 0: follower 1:leader

client.publish(f"Chenille-based-learning/Robots/{name_robot}/status", status, qos=1)

try:
    while True:
        target = random.randint(0, 1)  # Radius of ball

        client.publish(f"Chenille-based-learning/Robots/{name_robot}/BallRadius", target, qos=1)

        while status == -1:
            time.sleep(1)

        if status == 1:
            print("I am the Leader")
        else:
            print("I am the follower")

        time.sleep(1)

except KeyboardInterrupt:
    print("Disconnecting from the broker ...")
    client.publish("Chenille-based-learning/Server/population", i - 1, qos=2, retain=True)
    client.disconnect()
    client.loop_stop()
