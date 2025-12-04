from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

import time
import json
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

# Імпорт бібліотек Azure IoT
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# Налаштування сенсорів
adc = ADC()
relay = GroveRelay(110)

# рядок підключення до Azure IoT Hub
connection_string = "HostName=soil-moisture-sensor-ShvetsRoman.azure-devices.net;DeviceId=soil-moisture-sensor;SharedAccessKey=4Ak5fyP0C2dQYfoUEolDh9O8usQVch38lTIYAuqnXTg="


# --- Функція для обробки команд (Direct Methods) ---
def handle_method_request(request):
    print("Direct method received - ", request.name)

    if request.name == "relay_on":
        relay.on()
        print("Relay turned ON")
    elif request.name == "relay_off":
        relay.off()
        print("Relay turned OFF")

    # Відправка звіту в Azure, що команда виконана успішно (HTTP 200)
    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


# --- Ініціалізація клієнта Azure ---
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

# Прив'язка обробника команд до клієнта
device_client.on_method_request_received = handle_method_request

print('Connecting to Azure IoT Hub...')
device_client.connect()
print('Connected to Azure!')

# --- Основний цикл ---
while True:
    # Зчитування даних з CounterFit
    soil_moisture = adc.read(109)

    # Створення повідомлення для Azure
    message = Message(json.dumps({'soil_moisture': soil_moisture}))

    # Відправка телеметрії
    device_client.send_message(message)
    print(f"Sent telemetry to Azure: {message}")

    time.sleep(10)