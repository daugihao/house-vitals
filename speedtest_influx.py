#import adafruit_dht
#import board
import re
import subprocess
from influxdb import InfluxDBClient

response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
#dhtDevice = adafruit_dht.DHT11(board.D17)

ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')
#try:
#    temperature = dhtDevice.temperature
#    humidity = dhtDevice.humidity
#except RuntimeError as error:
#    print(error.args[0])

speed_data = [
        {
            "measurement": "internet_speed",
            "tags": {
                "host": "RaspberryPi"
                },
            "fields": {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping),
#               "temperature": float(temperature),
#               "humidity": float(humidity)
                }
            }
        ]

client = InfluxDBClient('localhost', 8086, 'speedmonitor', 'pimylifeup', 'internetspeed')

client.write_points(speed_data)

