import paho.mqtt.client as mqtt


# Mqtt servers infos

mqttBroker = ""


MyClient = mqtt.client("MyClient")

MyClient.connect(mqttBroker)


while True:


    break