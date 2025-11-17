import json
import time
import paho.mqtt.client as mqtt
import threading

# Налаштування MQTT
id = '6e6d3417-f9e7-4337-9176-b184333de774'
client_name = id + 'soil_moisture_sensor_server'
client_telemetry_topic = id + '/telemetry'
client_command_topic = id + '/commands'

# Час для циклу поливу
water_time = 5
wait_time = 20


def send_relay_command(client, state):
    command = {'relay_on': state}
    print(f"Sending message: {command}")
    client.publish(client_command_topic, json.dumps(command))


def control_relay(client):
    print("Unsubscribing from telemetry")
    client.unsubscribe(client_telemetry_topic)

    send_relay_command(client, True)
    time.sleep(water_time)
    send_relay_command(client, False)

    print(f"Waiting {wait_time}s for water to settle...")
    time.sleep(wait_time)

    print("Subscribing to telemetry")
    client.subscribe(client_telemetry_topic)


def handle_telemetry(client, userdata, message):
    payload_str = message.payload.decode()
    print("Message received:", payload_str)

    try:
        payload = json.loads(payload_str)

        if 'soil_moisture' in payload:
            soil_moisture = payload['soil_moisture']

            if soil_moisture > 417:
                print("Soil moisture > 417. Starting watering cycle.")
                threading.Thread(target=control_relay, args=(client,)).start()
            else:
                print("Soil moisture is OK.")

    except Exception as e:
        print(f"Error processing message: {e}")


# Ініціалізація MQTT клієнта
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_name)
mqtt_client.on_message = handle_telemetry

print("Server connecting to MQTT broker...")
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()
mqtt_client.subscribe(client_telemetry_topic)
print(f"Server subscribed to topic: {client_telemetry_topic}")

print("Soil moisture server started, waiting for data...")

try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Server disconnected.")