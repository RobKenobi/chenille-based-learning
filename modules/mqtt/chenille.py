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

name_robot = "Chenille"
client = mqtt.Client(name_robot, clean_session=True)

client.on_connect = on_connect

client.connect(broker, broker_port, keepalive=10)

client.loop_start()  # Start the loop

while Connected != True:  # Wait for the client to connect
    time.sleep(1)

try:
    while True:
        client.publish(f"Chenille-based-learning/number_of_active_robots", 1)
        client.subscribe(f"publisher.connect/Chenille/Leader")
        time.sleep(1)

except KeyboardInterrupt:
    print("Disconnecting from the broker ...")
    client.disconnect()
    client.loop_stop()
    print("Disconnected from the broker")
