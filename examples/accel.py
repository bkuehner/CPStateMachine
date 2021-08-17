import time
from StateMachine import StateMachine
from StateMachineManager import StateMachineManager
from random import randrange
from adafruit_circuitplayground import cp

timeLimit = 5
lastTime = time.time()

timeDelay = 1

currentPixel = -1

def selectRandomLed():
    turnOffAllPixels()
    global currentPixel
    temp = randrange(10)
    while( currentPixel == temp):
        temp = randrange(10)
    currentPixel = temp

    cp.pixels[currentPixel] = (0,0,255)
    time.sleep(timeDelay)
    global lastTime
    lastTime = time.time()
    

def checkTilt():
    x, y, z = cp.acceleration
    if currentPixel == -1:
        return False
    if (currentPixel == 2 or currentPixel == 7):
        return (x<-2 if currentPixel == 7 else x>2 )
    elif (currentPixel >= 3 and currentPixel <= 6):
        return (y > 2 and (x<-2 if currentPixel >= 5 else x>2 ))
    else:
        return  (y < -2 and (x<-2 if currentPixel >= 8 else x>2 ))


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

        
def checkTime():
    return (lastTime + timeLimit) < time.time()

smManager = StateMachineManager()


sm = smManager.CreateStateMachine("accel") 

print("created sm")
sm.AddState("start", selectRandomLed)
sm.AddState("state1",selectRandomLed)
sm.AddState("state2", selectRandomLed)
sm.AddState("exit",lambda: blinkAllPixels((0,255,0),4))

sm.AddTransition("start", checkTilt, "state1", None)
sm.AddTransition("state1", checkTilt, "state2", None)
sm.AddTransition("state2", checkTilt, "exit", None)

sm.AddTransition("state2", checkTime, "state1", lambda: blinkAllPixels((255,0,0),1))
sm.AddTransition("state1", checkTime, "start", lambda: blinkAllPixels((255,0,0),1))


sm.SetState("start")

while True:
    smManager.Update()



