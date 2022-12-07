import time
import paho.mqtt.client as mqtt
from multiprocessing import Process

Connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print("oh")
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


broker = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("HiveMind", clean_session=False)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port, keepalive=60)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    time.sleep(1)

client.subscribe("publisher.connect/#")

try:
    while True:
        client.publish("Chenille-based-learning/HiveMind/number_of_chenille", 1)

        time.sleep(1)

except KeyboardInterrupt:
    print("Disconnecting from the broker ...")
    client.disconnect()
    client.loop_stop()
    print("Disconnected from the broker")
