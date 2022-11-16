import time
import paho.mqtt.client as mqtt
import random
import numpy as np


#broker = "123a425d9b0748a39d2d27a7c2d4b7eb.s2.eu.hivemq.cloud"
#broker_port = 8883

broker = "broker.hivemq.com"
#broker = "mqtt.eclipseprojects.io"
broker_port = 1883


client = mqtt.Client("Client_pub")

client.connect(broker, broker_port)

name_robot="Robot1"
while True:
    number = random.randint(0, 10)
    client.publish(f"Chenille-based-learning/{name_robot}/Leader", 1)
    client.publish(f"Chenille-based-learning/{name_robot}/x", number)
    client.publish(f"Chenille-based-learning/{name_robot}/y", number+1)
    client.publish(f"Chenille-based-learning/{name_robot}/ball/d_robot", number + 1)
    client.publish(f"Chenille-based-learning/{name_robot}/ball/dx_cam", number + 1)
    client.publish(f"Chenille-based-learning/{name_robot}/ball/dy_cam", number + 1)
    client.publish(f"Chenille-based-learning/{name_robot}/ball/orientation", number + 1)
    time.sleep(1)
