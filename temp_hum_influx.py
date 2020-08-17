import adafruit_dht
import board
from time import sleep
from influxdb import InfluxDBClient

attempts = 0

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
        
        
        speed_data = [
                {
                    "measurement": "internet_speed",
                    "tags": {
                        "host": "RaspberryPi"
                        },
                    "fields": {
                        "temperature": float(temperature),
                        "humidity": float(humidity)
                        }
                }
                ]
        
        client = InfluxDBClient('localhost', 8086, 'speedmonitor', 'pimylifeup', 'internetspeed')
        client.write_points(speed_data)
        
        break
    
    except:
        attempts += 1
        sleep(1)

