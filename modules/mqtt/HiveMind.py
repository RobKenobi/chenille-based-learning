import time
import paho.mqtt.client as mqtt
import json
import threading

Connected = False
leader = 0
population = []

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
    population.append(json.loads(message.payload))
    # print("message topic=", message.topic)
    # print("message qos=", message.qos)
    # print("message retain flag=", message.retain)


def check_population(client, userdata, message):
    print("Current population:", str(message.payload.decode()))


def on_disconnect(client, userdata, rc):
    print("Disconnected to the broker")


broker = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("HiveMind", clean_session=False)

client.on_connect = on_connect

# client.message_callback_add()
client.message_callback_add("Chenille-based-learning/HiveMind/population", check_population)
client.message_callback_add("Chenille-based-learning/Swarm/#", on_message)
# client.on_message = on_message
# client.on_publish = on_publish
client.on_disconnect = on_disconnect

client.connect(broker, broker_port, keepalive=60)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    print(population)
    time.sleep(1)

client.subscribe("Chenille-based-learning/Swarm/#")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
