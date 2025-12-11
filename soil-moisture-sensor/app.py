from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)

import time
import json
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

# Імпорт бібліотек Azure IoT
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse, X509

# Налаштування сенсорів
adc = ADC()
relay = GroveRelay(110)

HOST_NAME = "soil-moisture-sensor-ShvetsRoman.azure-devices.net"
DEVICE_ID = "soil-moisture-sensor-x509-RomanShvets"
x509 = X509(
    cert_file="./soil-moisture-sensor-x509-RomanShvets-cert.pem",
    key_file="./soil-moisture-sensor-x509-RomanShvets-key.pem"
)
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
device_client = IoTHubDeviceClient.create_from_x509_certificate(
    x509=x509,
    hostname=HOST_NAME,
    device_id=DEVICE_ID
)

# Прив'язка обробника команд до клієнта
device_client.on_method_request_received = handle_method_request

print('Connecting to Azure IoT Hub using X.509...')
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