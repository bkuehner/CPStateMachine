import time
from StateMachine import StateMachine
from StateMachineManager import StateMachineManager
from random import randrange
from adafruit_circuitplayground import cp

timeDelay = 2

lastTime = time.time()
currentpixel = -1

def randomizeBtn():
    time.sleep(2)
    global currentpixel
    currentpixel = randrange(2)*5+2
    cp.pixels[currentpixel] = (255,0,0)
    
    global lastTime
    lastTime = time.time()
    
def checkTime():
    if time.time() > lastTime + timeDelay:
        cp.pixels[currentpixel] = (0,255,0)

def blinkAllPixels(color, blinks):
    for x in range(blinks):
        for i in range(10):
            cp.pixels[i] = color
        time.sleep(.5)
        turnOffAllPixels()
        time.sleep(.5)

def checkButton(resetTransition = False):
    currentBtn = cp.button_b if currentpixel == 7 else cp.button_a
    otherBtn = cp.button_b if currentpixel == 2 else cp.button_a
    if (currentBtn):
        if not resetTransition:
            return cp.pixels[currentpixel] == (0,255,0)
        else:
            return cp.pixels[currentpixel] == (255,0,0)
    if resetTransition and otherBtn:
        return True
    return False

def turnOffAllPixels():
    for i in range(10):
        cp.pixels[i] = (0,0,0)


smManager = StateMachineManager()


sm = smManager.CreateStateMachine("led") 


sm.AddState("start", randomizeBtn, checkTime)
sm.AddState("state1",randomizeBtn, checkTime)
sm.AddState("state2", randomizeBtn, checkTime)
sm.AddState("exit",lambda: blinkAllPixels((0,255,0),4))

sm.AddTransition("start", checkButton, "state1", lambda: blinkAllPixels((0,255,0),1))
sm.AddTransition("state1", checkButton, "state2", lambda: blinkAllPixels((0,255,0),1))
sm.AddTransition("state2", checkButton, "exit", lambda: blinkAllPixels((0,255,0),1))

sm.AddTransition("state1", lambda: checkButton(True), "start", lambda: blinkAllPixels((255,0,0),1))
sm.AddTransition("state2", lambda: checkButton(True), "start", lambda: blinkAllPixels((255,0,0),1))
sm.AddTransition("start", lambda: checkButton(True), "start", lambda: blinkAllPixels((255,0,0),1))


sm.SetState("start")

while True:
    smManager.Update()



