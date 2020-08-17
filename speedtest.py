import os
import re
import subprocess
import time

response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')
temperature = None
humidity = None

try:
    f = open('/home/pi/repos/speedtest/speedtest.csv', 'a+')
    if os.stat('/home/pi/repos/speedtest/speedtest.csv').st_size == 0:
        f.write('Date,Time,Ping (ms),Download (Mbits/s),Upload (Mbit/s),Temperature (C),Humidity (\%)\r\n')
except:
    pass

f.write('{},{},{},{},{},{},{}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), ping, download, upload, temperature, humidity))
