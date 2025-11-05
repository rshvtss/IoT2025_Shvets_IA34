import json
import time
import paho.mqtt.client as mqtt

from os import path
import csv
from datetime import datetime

id = '7a79b77a-b9ae-4ac0-af6c-75fb81e8e53a'
client_telemetry_topic = id + '/temperature'
client_name = id + 'temperature_sensor_server'

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)

mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

# --- CSV setup ---
temperature_file_name = 'temperature.csv'
fieldnames = ['date', 'temperature']

if not path.exists(temperature_file_name):
    with open(temperature_file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

# --- MQTT handler ---
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    with open(temperature_file_name, mode='a') as temperature_file:
        temperature_writer = csv.DictWriter(temperature_file, fieldnames=fieldnames)
        temperature_writer.writerow({
            'date': datetime.now().astimezone().replace(microsecond=0).isoformat(),
            'temperature': payload['temperature']
        })

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

print("Temperature server started, waiting for data...")

while True:
    time.sleep(2)
