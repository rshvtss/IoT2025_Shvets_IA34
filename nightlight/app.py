from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)
import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

light_sensor = GroveLightSensor(109)

led = GroveLed(110)
while True:
    light = light_sensor.light
    print('Light level:', light)
    if light < 109:
        led.on()
    else:
        led.off()

    time.sleep(3)