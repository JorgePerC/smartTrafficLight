""" 
Code to control an rPi HW through a REST service. 
"""             
# GroovePi libs             
import time   
from grovepi import *       
# Flask server imports      
import json   
from flask import Flask     
from flask import request, jsonify        
app = Flask(__name__)       

# Connect the Grove LED to digital port D4
ledPin = 4       
           
# HOME PAGE   
@app.route("/")             
def hello():  
        string = "Welcome my friend! \n"  
        string += "This example will blink a Grove LED connected to the GrovePi+ on the port D{}.\n".format(ledPin)
        string += "If you're having trouble seeing the LED blink, be sure to check the LED connection and the port number."   
        string += "You may also try reversing the direction of the LED on the sensor."            
        string += "Connect the LED to the D{} port !".format(ledPin)     
        return string


# READ        
@app.route('/blue_led/status',methods=['GET'])  
def getJedi():
        return "Is the LED ON? {}".format(digitalRead(ledPin))    

# CREATE      
"""           
Until now, its not necessary.             
"""           

#UPDATE       
@app.route('/blue_led/status', methods=['PUT']) 
def update_jedi():          
      # Recieved input    
      request_data = request.get_json() 
      # Check if tag is on input        
      if 'turnOn' not in request_data.keys():         
            return json.dumps({'message': 'Try with the "turnOn" tag'})         
        # Type is not boolean             
      if not isinstance(request_data['turnOn'], int): 
            return json.dumps({'message': 'invalid data'})        
        # Update LED status 
      try:  
            s = request_data['turnOn']
            digitalWrite(ledPin, s)      
      except IOError:             # Print "Error" if communication error encountered            
            return ("Error trying to change state") 
      return "Status set to: {}".format(s)           

# Delete      
"""           
Until now, its not necessary.             
"""           
# ==============================================================================================  
if __name__ == "__main__":  
        app.run(host="0.0.0.0", port=5001)   