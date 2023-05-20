

import os
import serial
import serial.tools.list_ports as list_ports

import time
import datetime
from datetime import date


from paho.mqtt import client as mqtt_client



broker_address = "141.145.219.166"
port = 1883
user = "SNSlab"
password = "SNSlab"



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("Python")
    client.username_pw_set(user, password=password)
    client.on_connect = on_connect
    client.connect(broker_address, port)
    return client


def publish_mqtt(client, topic, message):

    result = client.publish(topic, message)
        # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    #msg_count += 1



def main():
    client = connect_mqtt()
    client.loop_start()

    # give some time after connect
    time.sleep(1)
    
    #topic = "mqtt/test"
    topic = "SNSlabs/temperature_1"
    message = 69
    
    publish_mqtt(client, topic, message)


if __name__ == '__main__':
    main()