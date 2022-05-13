# Import all the components
from grovepi import *

# Physical connections
        # Red, yellow, green
ledPins = {"Red": 4, "Yellow": 3, "Green": 2}
    # Ultrasonic sensor
ultraSoundPin = 6

def turnOnIndividualLED(color):
        for i in ledPins:
                if color == i:
                        digitalWrite(ledPins[i], 1)
                else:
                        digitalWrite(ledPins[i], 0)

while True:
        dist = ultrasonicRead(ultraSoundPin)
        if dist > 300:
                turnOnIndividualLED("Green")
        elif dist > 90:
                turnOnIndividualLED("Yellow")
        else:
                turnOnIndividualLED("Red")

        print(dist)