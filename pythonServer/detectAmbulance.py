from operator import concat
from time import sleep
import requests
import json
import keyboard

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