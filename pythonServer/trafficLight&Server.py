""" 
Code to control an rPi 
traffic light through a REST service. 
"""  
# Run code before code finishes 
import atexit
# Threading
import threading
from operator import truediv
from time import sleep
# Traffic light class
from TrafficLight import TrafficLight
from grovepi import * 

# Flask server imports
import json
from flask import Flask  
from flask import request, jsonify  

# ===================== INIT =====================
# Valid JSON values:
jsonValid = ["ambulance", "status","red_led", "yellow_led", "green_led", "turnOff", "stopTraffic"]
global ambulance_passing
ambulance_passing = False

# App initiatlization
app = Flask(__name__)

# Physical connections:
tfLight = TrafficLight(4, 3, 2)
    # Ultrasonic sensor
ultraSoundPin = 6

# Function to run at end
def exit_handler():
    # Turn off all LEDs
    tfLight.turnOff()
    print ('The service is offline.')
    
# ===================== SERVER =====================
# HOME PAGE
@app.route("/") 
def hello():  
    string = "Welcome my friend! \n"  
    string += "With this website wu'll be able to control an inteligent traffic light"   
    return string

# ============= GET =============
# READ traffic lights         
@app.route('/<color>_led/status',methods=['GET'])  
def getGreen(color):
    return tfLight.getColorStatus_(color)

@app.route('/trafficLight/status',methods=['GET'])  
def getLight():
    return tfLight.getColor_()

# READ ultrasonicSensor
@app.route('/ultrasound/meas',methods=['GET'])  
def getDist():
    return "Dist: {}".format(ultrasonicRead(ultraSoundPin)) 

# Read ambulance incomming:
@app.route('/api/ambulance_near',methods=['GET'])
def getAmbulance_near():
    global ambulance_passing
    ambulance_passing = True
    return "Is ambulance near? {}".format(ambulance_passing)
         
# ============= SET =============
#UPDATE
@app.route('/<color>_led/status',methods=['PUT'])  
def setColor(color):
    request_data = request.get_json() 
    # Check if tag is on input        
    if color not in ["red", "green", "yellow"]:
        return json.dumps({'message': 'You entered a wrong color'})
    for k in request_data:
        if k not in jsonValid:         
            return json.dumps({'message': 'Try with any of the {} tags'.format(jsonValid)})
    # Type is not boolean             
    # if not isinstance(request_data['turnOn'], int): 
    #     return json.dumps({'message': 'invalid data'}) 
    s = request_data["status"]
    # Update LED status 
    return tfLight.setColorStatus_(color, s)

@app.route('/trafficLight/status', methods=['PUT']) 
def stopExec():
    # Recieved input    
    request_data = request.get_json() 
    # Check if tag is on input        
    for k in request_data:
        if k not in jsonValid:         
            return json.dumps({'message': 'Try with any of the {} tags'.format(jsonValid)})     
                # Type is not boolean
    if not isinstance(request_data['stopTraffic'], int): 
        return json.dumps({'message': 'invalid data'})        
                # Update LED status 
    s = request_data['stopTraffic']
    return tfLight.setColor_("red") 

# Ambulance:
@app.route('/api/ambulance_near', methods=['PUT'])
def setAmbulance_near():
    # Recieved input    
    request_data = request.get_json() 
    # Check if tag is on input        
    for k in request_data:
        if k not in jsonValid:         
            return json.dumps({'message': 'Try with any of the {} tags'.format(jsonValid)})     
                # Type is not boolean
    if not isinstance(request_data['ambulance'], int): 
        return json.dumps({'message': 'invalid data'})        
                # Update LED status 
    s = request_data['ambulance']
    
    global ambulance_passing
    ambulance_passing = False if s == 0 else True
    dist = ultrasonicRead(ultraSoundPin)
    return "Set ambulance near to: {}. The nearest car is at: {}".format(ambulance_passing, dist)

# CREATE      
"""           
Could we force the setup of new hardware?
"""  
# Delete      
"""           
Until now, its not necessary.             
"""      
# ============= TFLIGHT BEHAVIOUR =============
def nextColor():
    pattern = ["green", "yellow", "red"]
    
    actual = tfLight.getColor_()
    
    # Increment idx
    next = pattern.index(actual) + 1

    # Keep color in boundaries
    if next >= len(pattern):
        next = 0
    # Show next color 
    tfLight.setColor_(pattern[next])

def cycle():
    global ambulance_passing
    current = 0
    duration = 3
    while True:
        if ambulance_passing:
            tfLight.setColor_("yellow")
            sleep(1)
            while ambulance_passing:
                tfLight.setColor_("red")
                sleep(1)            
        else:
            while True:
                current = current + 1
                sleep(1)
                if current == duration:
                    nextColor()
                    current = 0
                if ambulance_passing:
                    break
# ==============================================================================================  
if __name__ == "__main__":  
    # Turn off at exit
    atexit.register(exit_handler)
    
    # Multi thread operation
    thr = threading.Thread(target=cycle, args=(), kwargs={})
    thr.start()

    #Init traffic light, to avoid error
    tfLight.setColor_("green")
    
    app.run(host="0.0.0.0", port=5001) 
