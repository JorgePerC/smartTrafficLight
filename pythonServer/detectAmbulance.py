from operator import concat
from time import sleep
import requests
import json
import keyboard

# TODO: Actually detect ambulance sound
# https://towardsdatascience.com/hands-on-signal-processing-with-python-9bda8aad39de
# https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python
# https://www.worldresearchlibrary.org/up_proc/pdf/1803-153578318109-14.pdf


def makeUrl(dir, rpiIP = '192.168.1.80', serverPort = '5001'):
    return "http://" + rpiIP + ":" + serverPort + dir

lastColor = ""

while True:
    if keyboard.is_pressed('y'):
        r = requests.put(makeUrl("/api/ambulance_near") , json= {"ambulance": 1})
        print(r.text)
    if keyboard.is_pressed('n'):
        r = requests.put(makeUrl("/api/ambulance_near") , json= {"ambulance": 0})
        print(r.text)
    response = requests.get(makeUrl("/trafficLight/status"))
    if lastColor != response.text:
        print(response.text)
    lastColor = response.text
    sleep(.1)
