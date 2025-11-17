from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

import time
import json
import paho.mqtt.client as mqtt
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

# Налаштування сенсорів
adc = ADC()
relay = GroveRelay(110)  # Пін реле

# Налаштування MQTT
id = '6e6d3417-f9e7-4337-9176-b184333de774'
client_name = id + 'soil_moisture_sensor_client'
client_telemetry_topic = id + '/telemetry'
client_command_topic = id + '/commands'


def on_message(client, userdata, msg):
    print(f"Received command on topic {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())

        if 'relay_on' in data:
            if data['relay_on']:
                print("Command: Turning relay ON")
                relay.on()
            else:
                print("Command: Turning relay OFF")
                relay.off()

    except Exception as e:
        print(f"Error handling command: {e}")


# Ініціалізація MQTT клієнта
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.on_message = on_message

print("Connecting to MQTT broker...")
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()
mqtt_client.subscribe(client_command_topic)
print(f"Subscribed to topic: {client_command_topic}")

print("MQTT connected! Starting sensor loop...")
while True:
    try:
        soil_moisture = adc.read(109)
        telemetry = json.dumps({"soil_moisture": soil_moisture})

        print(f"Sending telemetry: {telemetry}")
        mqtt_client.publish(client_telemetry_topic, telemetry)

        time.sleep(10)

    except KeyboardInterrupt:
        print("Stopping application...")
        break

mqtt_client.loop_stop()
print("Application stopped.")