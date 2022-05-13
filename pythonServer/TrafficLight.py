# GroovePi libs 
from grovepi import * 


class TrafficLight :
    def __init__(self, r, y, g):
        # Physical connections
        self.ledPins = {"red": r, "yellow": y, "green": g} 
        self.ledStatus = {"red": 0, "yellow": 0, "green": 0} 

        self.turnOff()
    
    def turnOff(self) :
        try:  
            for led in self.ledPins.values():
                digitalWrite(led, 0)
            for k in self.ledStatus.keys():
                self.ledStatus[k] = 0   
        except IOError:     # Print "Error" if communication error encountered            
            return ("Error trying to change state") 
        return "The semaphore is off"
        

    def getColorStatus(self, color):
        return "Is the {} LED ON? {}".format(color, digitalRead(self.ledPins[color]))

    def getColorStatus_(self, color):
        return "Is the {} LED ON? {}".format(color, self.ledStatus[color])


    def getColor(self):
        for k in self.ledPins.keys():
            if digitalRead(self.ledPins[k]) == 1:
                return k #"The actual color is {}".format(color)
        return "Error, no color is turned on"
    
    def getColor_(self):
        for k in self.ledPins.keys():
            #print(k, self.ledPins[k], digitalRead(self.ledPins[k]), self.ledStatus[k])
            if self.ledStatus[k] == 1:
                return k #"The actual color is {}".format(color)
        return "Error, no color is turned on"


    # Function to turn only one LED at a time
    def setColor(self, color):
        try:
            for i in self.ledPins:
                if color == i:
                    digitalWrite(self.ledPins[i], 1)
                else:
                    digitalWrite(self.ledPins[i], 0)
        except IOError:  
            return ("Error trying to change state") 
        return "Set {} LED on.".format(color)
    def setColor_(self, color):
        try:
            for i in self.ledPins:
                if color == i:
                    digitalWrite(self.ledPins[i], 1)
                    self.ledStatus[i] = 1
                else:
                    digitalWrite(self.ledPins[i], 0)
                    self.ledStatus[i] = 0
        except IOError:  
            return ("Error trying to change state") 
        return "Set {} LED on.".format(color)


    def setColorStatus(self, color, status):
        # Update LED status 
        try:  
            digitalWrite(self.ledPins[color], status)  
            self.ledStatus[color] = status    
        except IOError:     # Print "Error" if communication error encountered            
            return ("Error trying to change state") 
        return "Set {} to: {}".format(color, status)

if __name__ == "__main__":
    a = TrafficLight(4, 3, 2)