import json
import time
import paho.mqtt.client as mqtt
id = 'f88b0c4e-a8c3-4525-a02c-d31bafe43a7b'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_server'
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    command = {'led_on': payload['light'] < 109}
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry
while True:
    time.sleep(2)