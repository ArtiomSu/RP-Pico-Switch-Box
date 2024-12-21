from hardware import Hardware
from tools import generate_random_booleans
from tools import get_last_output_sum
import time

gameRunning = True
gameDeadState = 100
gameState = 0
hardware = Hardware()
updateInterval = 100 * 1_000_000
lastUpdateTime = time.monotonic_ns()
framesCount = 0
level = 1
levelMax = 5
seed = 0
lastOuputSum = -1
gotLevelSeed = False
levelSeconds = 0
gameSeconds = 0

for i in range(10):
    out = generate_random_booleans(4, i) 
    print(f"{out} {get_last_output_sum(out)}")


def handleLevels():
    global hardware
    global gameState
    global framesCount
    global level
    global gameDeadState
    global levelMax
    global seed
    global lastOuputSum
    global gotLevelSeed
    global levelSeconds
    hardware.display.printText(f"Level {level}/{levelMax}", "centre", 0, "centre")
    hardware.display.printText(f"{levelSeconds} Seconds", "bottom", 1, "centre")
    switchOuts = hardware.getSwitchesOutput()
    nowOutPutSum = lastOuputSum
    levelOuts = generate_random_booleans(len(switchOuts), seed)
    if not gotLevelSeed:
        while nowOutPutSum == lastOuputSum:
            seed = seed + 1
            levelOuts = generate_random_booleans(len(switchOuts), seed)
            # set to true so that the dead game state works
            if level >= levelMax and levelOuts[len(hardware.switchAndLeds) -1] == False:
                nowOutPutSum = lastOuputSum
                print("adjusting for last level")
            else:
                nowOutPutSum = get_last_output_sum(levelOuts)
            print(f"-----------------------------")
            print(f"level {level} last out is {lastOuputSum} now out is {nowOutPutSum}")
            print(f"-----------------------------")
            
        gotLevelSeed = True
        lastOuputSum = nowOutPutSum

    #print(f" level outs {levelOuts}")
    numCorrect = 0
    normalLedIndexToUse = 0
    for i in range(len(switchOuts)):
        normalLedIndexToUse = i
        if(i >= 2):
            normalLedIndexToUse = normalLedIndexToUse + 1
        if switchOuts[i] == levelOuts[i]:
            numCorrect = numCorrect + 1
            hardware.normalLeds[normalLedIndexToUse].setLed(True)
        else:
            hardware.normalLeds[normalLedIndexToUse].setLed(False)
    
    #print(f"num correct is {numCorrect}")
    
    if numCorrect == len(switchOuts):
        gameState = gameState + 1
        

def main():
    global gameRunning
    global gameDeadState
    global gameState
    global hardware
    global updateInterval
    global lastUpdateTime
    global framesCount
    global level
    global levelMax
    global gotLevelSeed
    global gameSeconds
    global levelSeconds
    gameStartedTime = 0
    levelStartedTime = 0
    while gameRunning:
        currentTime = time.monotonic_ns()
        deltaTime = currentTime - lastUpdateTime
        if(deltaTime >= updateInterval):
            #print("updating frame")
            if gameState == 0:
                if hardware.startupAnimation(framesCount):
                    gameState = gameState + 1
                    hardware.enableSwitchInput()
                    gameStartedTime = time.monotonic_ns()
                    levelStartedTime = time.monotonic_ns()
            elif gameState == 1:
                levelSeconds = (currentTime - levelStartedTime) // 1_000_000_000
                handleLevels()
            elif gameState == 2:
                # level finished
                if level >= levelMax:
                    gameSeconds = (currentTime - gameStartedTime) // 1_000_000_000
                    hardware.display.printText(f"You Won", "centre", 0, "centre")
                    hardware.display.printText(f"In {gameSeconds} Seconds", "bottom", 1, "centre")
                    time.sleep(5)
                    level = 1
                    gotLevelSeed = False
                    gameState = gameDeadState
                    hardware.turnOffAllLeds()
                    hardware.display.clear()
                else: 
                    hardware.turnOffAllLeds()
                    hardware.normalLeds[2].setLed(True)
                    hardware.display.printText(f"Level {level} complete", "centre", 0, "centre")
                    level = level + 1
                    gotLevelSeed = False
                    time.sleep(1)
                    hardware.normalLeds[2].setLed(False)
                    hardware.enableSwitchInput()
                    gameState = gameState - 1
                    levelStartedTime = time.monotonic_ns()
            elif gameState == gameDeadState:
                restart = hardware.deadState(framesCount)
                if restart:
                    framesCount = -1
                    gameState = 0
            lastUpdateTime = currentTime
            framesCount = framesCount + 1
        #print(f"loop running {time.monotonic_ns()}")
        time.sleep(0.001)

main()