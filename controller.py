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
    status[parameter] = state
    publisherClient.publish(MQTT_TOPIC, payload)

    return payload


status = {}


def on_message(_client, userdata, msg):
    global status
    print(f'Получено "{msg.payload.decode()}" из топика "{msg.topic}"')

    last_update = json.loads(msg.payload.decode())
    status.update(last_update)
    print(status)


subscriberClient = paho.Client(MQTT_CLIENT_ID + "_SUBSCRIBER")
subscriberClient.username_pw_set(MQTT_TOKEN)
subscriberClient.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
subscriberClient.subscribe(MQTT_TOPIC)
subscriberClient.on_message = on_message
Thread(target=subscriberClient.loop_forever).start()


def get_status() -> str:
    return json.dumps(status)
