import board
from display import Display
from ledNormal import LedNormal
from switchAndLed import SwitchAndLed
class Hardware:
    display = None
    normalLedsPins = [board.GP16, board.GP17, board.GP18, board.GP19 ,board.GP20]
    normalLedColours = ["red", "yellow", "green", "white", "blue"]
    switchLedPins = [board.GP15, board.GP14, board.GP13, board.GP12]
    switchPins = [board.GP11, board.GP10, board.GP9, board.GP8]
    switchColours = ["orange", "blue", "purple", "red"]

    normalLeds = []
    switchAndLeds = []

    def __init__(self):
        self.display = Display()

        normalLedCounter = 0
        for normalLedPin in self.normalLedsPins:
            self.normalLeds.append(LedNormal(normalLedPin, self.normalLedColours[normalLedCounter], normalLedCounter))
            normalLedCounter = normalLedCounter + 1
        
        for i in range(len(self.switchLedPins)):
            self.switchAndLeds.append(SwitchAndLed(self.switchLedPins[i], self.switchColours[i], i, self.switchPins[i], i))
    
    def turnOffAllLeds(self):
        for led in self.normalLeds:
            led.setLed(False)
        
        for led in self.switchAndLeds:
            led.setLed(False)

    def startupAnimationOled(self, frame, frameCount):
        self.display.animateText("+-------------+", frame, frameCount, "top", 0)
        self.display.animateText("| Switch  Box |", frame, frameCount, "centre", 1)
        self.display.animateText("| By ArtiomSu |", frame, frameCount, "bottom", 2)
        self.display.display.refresh()

    def startupAnimationLeds(self, frame):
        if frame < len(self.normalLeds):
            self.normalLeds[frame].setLed(True)
            if(frame > 0):
                self.normalLeds[frame - 1].setLed(False)
            return False

        self.normalLeds[len(self.normalLeds) -1].setLed(False)
        frame = frame - len(self.normalLeds)

        if frame < len(self.switchAndLeds):
            self.switchAndLeds[frame].setLed(True)
            if(frame > 0):
                self.switchAndLeds[frame - 1].setLed(False)
            return False

        self.switchAndLeds[len(self.switchAndLeds) -1].setLed(False)
        frame = frame - len(self.switchAndLeds)

        if frame < len(self.switchAndLeds):
            self.switchAndLeds[(len(self.switchAndLeds) - 1) - frame].setLed(True)
            if(frame > 0):
                self.switchAndLeds[len(self.switchAndLeds) - frame].setLed(False)
            return False
        
        self.switchAndLeds[0].setLed(False)
        frame = frame - len(self.switchAndLeds)

        if frame < len(self.normalLeds):
            self.normalLeds[(len(self.normalLeds) - 1) - frame].setLed(True)
            if(frame > 0):
                self.normalLeds[len(self.normalLeds) - frame].setLed(False)
            return False

        self.normalLeds[0].setLed(False)
        #self.turnOffAllLeds()
        return True

    def startupAnimation(self, frame):
        if frame == 0:
            self.display.clear()
        totalFrames = (len(self.normalLeds) * 2) + (len(self.switchAndLeds) * 2)
        self.startupAnimationOled(frame, totalFrames)
        if self.startupAnimationLeds(frame):
            self.display.clear()
            return True
        return False
    
    def enableSwitchInput(self):
        for led in self.switchAndLeds:
            led.setLed(True)

    def getSwitchesOutput(self):
        output = []
        for switch in self.switchAndLeds:
            output.append(switch.isSwitchOn())
        return output
    
    def turnOff(self):
        self.turnOffAllLeds()
        self.display.clear()

    def deadState(self, framesCount):
        switchOuts = self.getSwitchesOutput()
        restart = False
        lastIndex = len(self.switchAndLeds) - 1
        isOn = self.switchAndLeds[lastIndex].isOn()
        if isOn:
            if switchOuts[lastIndex] == False:
                restart = True
        if restart:
            self.turnOffAllLeds()
            return True
        else:
            # run this every 1 frames
            # if framesCount % 10 == 0:
            if framesCount % 1 == 0:
                self.switchAndLeds[lastIndex].setLed(not isOn)
        return False

