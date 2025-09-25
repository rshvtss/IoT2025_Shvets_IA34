from counterfit_connection import CounterFitConnection

CounterFitConnection.init('127.0.0.1', 5000)
import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

light_sensor = GroveLightSensor(109)
while True:
    light = light_sensor.light
    print('Light level:', light)
    time.sleep(1)