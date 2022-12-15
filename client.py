import websocket #import websockt library -> pip install websocket-client
import ssl # import ssl library (native)
import json # import json library (native)
from multipledispatch import dispatch # import the dispatch library to enable method overloading in python
import board
import neopixel
import rel

pixel_pin = board.D21 # the pin to which the LED strip is connected to
num_pixels = 24 # this specifies the TOTAL number of pixels (should be a multiple of 12. ie. 12, 24, 36, 48 etc)
ORDER = neopixel.GRB # set the color type of the neopixel
ledSegment = 6 # number of LEDs in a single segment
ledArray = [[[0 for i in range(3)] for j in range(ledSegment)] for z in range(4)] #the array which stores the pixel information

pixels = neopixel.NeoPixel( # create and initiate neopixel object
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)



def on_message(ws, message): # function which is called whenever a new message comes in
    print("received a message: ", message) # debug that we received a message
    json_data = json.loads(message) # incoming message is transformed into a JSON object
    updatePixels(json_data) # call function to update the neopixel strip

def on_error(ws, e): # function call when there is an error
    print("got an error: ",e)

def on_close(ws, e, d): # function call when the connection is closed (this should not happend currently as we are staying connected)
    print("### closed ###")
    print(e)
    print(d)

def on_open(ws): # function call when a new connection is established
    print("### open ###")

def on_ping(wsapp, message):
    print("Got a ping! A pong reply has already been automatically sent. ", message)

def on_pong(wsapp, message):
    print("Got a pong! No need to respond. ", message)

def updatePixels(json):
    iteration = 0 # reset number of iterations to 0. this is a helper variable to address different segments of the LED strip
    for ring in json["lights"]: # iterate through every ring object inside the JSON file

        l = len(json["lights"][ring]["colors"]) # figure out how many colors should be displayed
        if l == 1: # if one light needs to be displayed
            c1r = json["lights"][ring]["colors"]["1"]["r"] # get the red color value
            c1g = json["lights"][ring]["colors"]["1"]["g"] # get the green color value
            c1b = json["lights"][ring]["colors"]["1"]["b"] # get the blue color value
            
            setColorArray(iteration,c1r,c1g,c1b) # call the setColorArray function

        elif l == 2: # if two lights need to be displayed (gradient)
            c1r = json["lights"][ring]["colors"]["1"]["r"] # get the first red color value
            c1g = json["lights"][ring]["colors"]["1"]["g"] # get the first green color value
            c1b = json["lights"][ring]["colors"]["1"]["b"] # get the first blue color value

            c2r = json["lights"][ring]["colors"]["2"]["r"] # get the second red color value
            c2g = json["lights"][ring]["colors"]["2"]["g"] # get the second green color value
            c2b = json["lights"][ring]["colors"]["2"]["b"] # get the second blue color value
            
            setColorArray(iteration,c1r,c1g,c1b,c2r,c2g,c2b) # call the setColorArray function

        elif l == 3: # if three lights need to be displayed (gradient)
            c1r = json["lights"][ring]["colors"]["1"]["r"] # get the first red color value
            c1g = json["lights"][ring]["colors"]["1"]["g"] # get the first green color value
            c1b = json["lights"][ring]["colors"]["1"]["b"] # get the first blue color value

            c2r = json["lights"][ring]["colors"]["2"]["r"] # get the second red color value
            c2g = json["lights"][ring]["colors"]["2"]["g"] # get the second green color value
            c2b = json["lights"][ring]["colors"]["2"]["b"] # get the second blue color value
            
            c3r = json["lights"][ring]["colors"]["3"]["r"] # get the third red color value
            c3g = json["lights"][ring]["colors"]["3"]["g"] # get the third green color value
            c3b = json["lights"][ring]["colors"]["3"]["b"] # get the third blue color value
            
            setColorArray(iteration,c1r,c1g,c1b,c2r,c2g,c2b,c3r,c3g,c3b) # call the setColorArray function

        elif l == 4: # if four lights need to be displayed (gradient)
            c1r = json["lights"][ring]["colors"]["1"]["r"] # get the first red color value
            c1g = json["lights"][ring]["colors"]["1"]["g"] # get the first green color value
            c1b = json["lights"][ring]["colors"]["1"]["b"] # get the first blue color value
            
            c2r = json["lights"][ring]["colors"]["2"]["r"] # get the second red color value
            c2g = json["lights"][ring]["colors"]["2"]["g"] # get the second green color value
            c2b = json["lights"][ring]["colors"]["2"]["b"] # get the second blue color value
            
            c3r = json["lights"][ring]["colors"]["3"]["r"] # get the third red color value
            c3g = json["lights"][ring]["colors"]["3"]["g"] # get the third green color value
            c3b = json["lights"][ring]["colors"]["3"]["b"] # get the third blue color value
            
            c4r = json["lights"][ring]["colors"]["3"]["r"] # get the fourth red color value
            c4g = json["lights"][ring]["colors"]["3"]["g"] # get the fourth green color value
            c4b = json["lights"][ring]["colors"]["3"]["b"] # get the fourth blue color value
            
            setColorArray(iteration,c1r,c1g,c1b,c2r,c2g,c2b,c3r,c3g,c3b,c4r,c4g,c4b) # call the setColorArray function
        
        offset = iteration * ledSegment # calculate the offset to address the single neopixel strip as it were N number of strips

        for index in range(ledSegment): # for loop to run through the individual segments
            pixels[index+offset] = (ledArray[iteration][index][0],ledArray[iteration][index][1],ledArray[iteration][index][2]) # for each pixel on the LED strip, calculate the position of the color inside the three dimensional color array and assign it
        
        iteration += 1 # increase the iteration (ie. work on the next segment of the LED strip)
    
    pixels.show() # once done, update the led strip

# function to assign single color to array
@dispatch(int, int, int, int)
def setColorArray(iteration, c1r, c1g, c1b):
    for x in range(ledSegment): # cycle through the whole segment
        ledArray[iteration][x][0] = c1r # set the value of the red channel to the whole color array
        ledArray[iteration][x][1] = c1g # set the value of the green channel to the whole color array
        ledArray[iteration][x][2] = c1b # set the value of the blue channel to the whole color array

# function to assign two colors to array to create a gradient
@dispatch(int, int, int, int, int, int, int)
def setColorArray(iteration, c1r, c1g, c1b, c2r, c2g, c2b):
    for x in range(int(ledSegment/2)): # cycle through half of the segment (as we need to create a gradient, the other half of the segment is automatically calculated)
        ledArray[iteration][x + ((int(ledSegment/2))*0)][0] = int((x - 0) / ((int(ledSegment/2)) - 0) * (c2r - c1r) + c1r) # based on the position inside the color array, calculate the value of the red channel so it morphs from the first color to the second
        ledArray[iteration][x + ((int(ledSegment/2))*1)][0] = int((x - 0) / ((int(ledSegment/2)) - 0) * (c1r - c2r) + c2r)

        ledArray[iteration][x + ((int(ledSegment/2))*0)][1] = int((x - 0) / ((int(ledSegment/2)) - 0) * (c2g - c1g) + c1g) # based on the position inside the color array, calculate the value of the green channel so it morphs from the first color to the second
        ledArray[iteration][x + ((int(ledSegment/2))*1)][1] = int((x - 0) / ((int(ledSegment/2)) - 0) * (c1g - c2g) + c2g)

        ledArray[iteration][x + ((int(ledSegment/2))*0)][2] = int((x - 0) / ((int(ledSegment/2)) - 0) * (c2b - c1b) + c1b) # based on the position inside the color array, calculate the value of the blue channel so it morphs from the first color to the second
        ledArray[iteration][x + ((int(ledSegment/2))*1)][2] = int((x - 0) / ((int(ledSegment/2)) - 0) * (c1b - c2b) + c2b)

# function to assign three colors to array to create a gradient
@dispatch(int, int, int, int, int, int, int, int, int, int)
def setColorArray(iteration, c1r, c1g, c1b, c2r, c2g, c2b, c3r, c3g, c3b):
    for x in range(int(ledSegment/3)): # cycle through a third of the segment (as we need to create a gradient, the other two thirds of the segment are automatically calculated)
        ledArray[iteration][x + ((int(ledSegment/3))*0)][0] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c2r - c1r) + c1r) # based on the position inside the color array, calculate the value of the red channel so it morphs from the first color to the second and to the third
        ledArray[iteration][x + ((int(ledSegment/3))*1)][0] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c3r - c2r) + c2r)
        ledArray[iteration][x + ((int(ledSegment/3))*2)][0] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c1r - c3r) + c3r)

        ledArray[iteration][x + ((int(ledSegment/3))*0)][1] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c2g - c1g) + c1g) # based on the position inside the color array, calculate the value of the green channel so it morphs from the first color to the second and to the third
        ledArray[iteration][x + ((int(ledSegment/3))*1)][1] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c3g - c2g) + c2g)
        ledArray[iteration][x + ((int(ledSegment/3))*2)][1] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c1g - c3g) + c3g)

        ledArray[iteration][x + ((int(ledSegment/3))*0)][2] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c2b - c1b) + c1b) # based on the position inside the color array, calculate the value of the blue channel so it morphs from the first color to the second and to the third
        ledArray[iteration][x + ((int(ledSegment/3))*1)][2] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c3b - c2b) + c2b)
        ledArray[iteration][x + ((int(ledSegment/3))*2)][2] = int((x - 0) / ((int(ledSegment/3)) - 0) * (c1b - c3b) + c3b)

# function to assign four colors to array to create a gradient
@dispatch(int, int, int, int, int, int, int, int, int, int, int, int, int)
def setColorArray(iteration, c1r, c1g, c1b, c2r, c2g, c2b, c3r, c3g, c3b, c4r, c4g, c4b):
    for x in range(int(ledSegment/4)):  # cycle through a fourth of the segment (as we need to create a gradient, the other three quarters of the segment are automatically calculated)
        ledArray[iteration][x + ((int(ledSegment/4))*0)][0] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c2r - c1r) + c1r) # based on the position inside the color array, calculate the value of the red channel so it morphs from the first color to the second, to the third, and to the fourth
        ledArray[iteration][x + ((int(ledSegment/4))*1)][0] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c3r - c2r) + c2r)
        ledArray[iteration][x + ((int(ledSegment/4))*2)][0] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c4r - c3r) + c3r)
        ledArray[iteration][x + ((int(ledSegment/4))*3)][0] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c1r - c4r) + c4r)

        ledArray[iteration][x + ((int(ledSegment/4))*0)][1] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c2g - c1g) + c1g) # based on the position inside the color array, calculate the value of the green channel so it morphs from the first color to the second, to the third, and to the fourth
        ledArray[iteration][x + ((int(ledSegment/4))*1)][1] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c3g - c2g) + c2g)
        ledArray[iteration][x + ((int(ledSegment/4))*2)][1] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c4g - c3g) + c3g)
        ledArray[iteration][x + ((int(ledSegment/4))*3)][1] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c1g - c4g) + c4g)

        ledArray[iteration][x + ((int(ledSegment/4))*0)][2] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c2b - c1b) + c1b) # based on the position inside the color array, calculate the value of the blue channel so it morphs from the first color to the second, to the third, and to the fourth
        ledArray[iteration][x + ((int(ledSegment/4))*1)][2] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c3b - c2b) + c2b)
        ledArray[iteration][x + ((int(ledSegment/4))*2)][2] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c4b - c3b) + c3b)
        ledArray[iteration][x + ((int(ledSegment/4))*3)][2] = int((x - 0) / ((int(ledSegment/4)) - 0) * (c1b - c4b) + c4b)

if __name__ == "__main__": # main loop
    websocket.enableTrace(True) # print the connection details (for debugging purposes)
    ws = websocket.WebSocketApp("wss://qp-master-server.herokuapp.com/", # websocket URL to connect to
                              on_message = on_message, # what should happen when we receive a new message
                              on_error = on_error, # what should happen when we get an error
                              on_close = on_close, # what should happen when the connection is closed
                              on_ping = on_ping, # on ping
                              on_pong = on_pong) # on pong
    ws.on_open = on_open # call on_open function when the ws connection is opened
    ws.run_forever(dispatcher=rel, reconnect=5, ping_interval=15, ping_timeout=10, ping_payload="This is an optional ping payload", sslopt={"cert_reqs": ssl.CERT_NONE}) # run code forever and disable the requirement of SSL certificates
    rel.signal(2, rel.abort) # keyboard interrupt
    rel.dispatch() 
