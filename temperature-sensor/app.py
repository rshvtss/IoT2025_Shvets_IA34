from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

import json
import time
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt

sensor = DHT("11", 109)

id = '7a79b77a-b9ae-4ac0-af6c-75fb81e8e53a'
client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/temperature'
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)

mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

print("MQTT connected! Temperature telemetry sending...")

while True:
    _, temp = sensor.read()
    telemetry = json.dumps({'temperature': temp})

    print("Sending telemetry:", telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(10)
