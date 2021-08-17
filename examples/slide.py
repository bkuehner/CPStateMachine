import time
from StateMachine import StateMachine
from StateMachineManager import StateMachineManager
from random import randrange
from adafruit_circuitplayground import cp

timeDelay = 1

lastTime = time.time()
currentPos = 0
currentPixel = 0

def startState():
    global currentPixel
    currentPixel = 2 if cp.switch else 7
    global currentPos
    currentPos = 0
    global lastTime
    lastTime = time.time()

def updateState():
    global currentPos
    global currentPixel
    
    if (currentPos % 3 == 0):
        cp.pixels[currentPixel] = (0,255,0)
    elif (currentPos % 3 == 1):
        cp.pixels[currentPixel + 1] = (0,255,0)
        cp.pixels[currentPixel- 1] = (0,255,0)
    else:
        cp.pixels[currentPixel + 2] = (0,255,0)
        cp.pixels[currentPixel- 2] = (0,255,0)
    
    global timeDelay
    global lastTime
    if time.time() > lastTime + timeDelay:
        turnOffAllPixels()
        lastTime = time.time()
        currentPos += 1
        if currentPos % 3 == 0:
            timeDelay = 1
        if currentPos % 3 == 2:
            timeDelay = 2

def checkTransition():
    currentPixel

def blinkAllPixels(color, blinks):
    for x in range(blinks):
        for i in range(10):
            cp.pixels[i] = color
        time.sleep(.5)
        turnOffAllPixels()
        time.sleep(.5)

def turnOffAllPixels():
    for i in range(10):
        cp.pixels[i] = (0,0,0)


smManager = StateMachineManager()


sm = smManager.CreateStateMachine("led") 


sm.AddState("start", startState, updateState)

sm.AddTransition("start", lambda: (cp.switch if currentPixel == 7 else not cp.switch), "start",lambda: blinkAllPixels((0,255,0),4) )



sm.SetState("start")

while True:
    smManager.Update()



