
import serial.tools.list_ports
import json

import requests
from datetime import datetime

def SendToWeb(jsonik):
    try:
        r = requests.post(url=link, json=jsonik)
        pastebin_url = r.text
        print("The pastebin URL is: ", pastebin_url)
    except:
        print("Post request func error.")

link = 'https://pir2022.azurewebsites.net/api/PogodasPost'

print("Its a list of COM connected devices:")

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

print("Chose your COM (number):")

COM_port = 3 #input()
COM_port = 'COM3' #'COM' + COM_port
print(COM_port)
try:
    ser = serial.Serial(COM_port, 9600, timeout=4)
except:
    print("COM port is already used")
    print("Please terminate this connection and try again!")
    quit()

now = datetime.now()
date_time = now.strftime("'%m/%d/%YT%H:%M:%S'")

x = 1
badFrame = False
prevCuttedFrame = ''

while 1 :
    x = x + 1
    now = datetime.now()  # current date and time
    local_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    justGot = ser.read(121)
    print(justGot)
    try:
        new = json.dumps({**{"czas": local_time}, **json.loads(justGot)})
        new = json.loads(new)
        # print(new, type(new))
        SendToWeb(new)
    except:
        print("!!Faulty frame!!: ")


ser.close()
,