import adafruit_dht
import board
from math import log
from time import sleep
from influxdb import InfluxDBClient

attempts = 0
dew_point = {
        "b":18.678,
        "c":257.14
        }

while attempts < 3:
    try:
        dhtDevice = adafruit_dht.DHT22(board.D17)
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print(f"Temperature: {temperature}C")
        print(f"Relative Humidity: {humidity}%")

        if temperature == None:
            raise ValueError
        if humidity == None:
            raise ValueError
        
        
        y = log(humidity/100) + (dew_point['b']*temperature)/(dew_point['c'] + temperature)
        temperature_dewpoint = (dew_point['c']*y) / (dew_point['b'] - y)
        
        print(f"Dew Point Temperature: {temperature_dewpoint:.1f}C")

        speed_data = [
                {
                    "measurement": "internet_speed",
                    "tags": {
                        "host": "RaspberryPi"
                        },
                    "fields": {
                        "temperature": float(temperature),
                        "humidity": float(humidity),
                        "temperature_dewpoint": float(temperature_dewpoint)
                        }
                }
                ]
        
        client = InfluxDBClient('localhost', 8086, 'speedmonitor', 'pimylifeup', 'internetspeed')
        client.write_points(speed_data)
        
        break
    
    except Exception as e:
        print(e)
        attempts += 1
        sleep(1)

