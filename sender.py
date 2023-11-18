import json
from threading import Thread

import paho.mqtt.client as paho

from config import MQTT_BROKER, MQTT_CLIENT_ID, MQTT_TOKEN, MQTT_TOPIC, MQTT_PORT

publisherClient = paho.Client(MQTT_CLIENT_ID + "_PUBLISHER")
publisherClient.username_pw_set(MQTT_TOKEN)
publisherClient.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
Thread(target=publisherClient.loop_forever).start()


def publish(parameter: str, state: str) -> str:
    payload = json.dumps({parameter: state})
    publisherClient.publish(MQTT_TOPIC, payload)

    return payload


if __name__ == '__main__':
    while True:
        parameter, state = input().split()
        payload = '{' + f'"{parameter}":"{state}"' + '}'
        print(payload)
        publisherClient.publish(MQTT_TOPIC, payload)
