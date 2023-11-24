import time
import Adafruit_DHT
from scipy import stats
import numpy as np

from models import RackStats

rack_stats = RackStats()


def get_sensors():
    sensor = Adafruit_DHT.DHT22
    pin = 4
    loop = 20
    
    avg_humidity, avg_temperature = np.array([]), np.array([])
    for _ in range(loop):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            avg_humidity = np.append(avg_humidity, humidity)
            avg_temperature = np.append(avg_temperature, temperature)
            #print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(humidity, temperature))
        time.sleep(0.5)
    
    if avg_humidity.size == 0 or avg_temperature.size == 0:
        raise Exception('Failure to get sensor data')
    
    humidity_z_scores = stats.zscore(avg_humidity)
    temperature_z_scores = stats.zscore(avg_temperature)

    humidity_no_outliers = avg_humidity[np.abs(humidity_z_scores) < 3]
    temperature_no_outliers = avg_temperature[np.abs(temperature_z_scores) < 3]

    avg_humidity_mean = np.mean(humidity_no_outliers)
    avg_temperature_mean = np.mean(temperature_no_outliers)

    print('Avg Temp={0:0.1f}°C  Avg Humidity={1:0.1f}%'.format(avg_temperature_mean, avg_humidity_mean))
    return avg_temperature_mean, avg_humidity_mean


if __name__ == "__main__":
    try:
        temperature, humidity = get_sensors()
        rack_stats.addRecord(temperature, humidity)
    except:
        pass
