import digitalio

class SwitchAndLed:
    pin = None
    switchPin = None
    colour = None
    led = None
    switch = None
    index = None
    indexSwitch = None

    def __init__(self, pin, colour, index, switchPin, switchIndex):
        self.pin = pin
        self.switchPin = switchPin
        self.switch = switchIndex
        self.colour = colour
        self.index = index
        self.indexSwitch = switchIndex
        self.led = digitalio.DigitalInOut(self.pin)
        self.led.direction = digitalio.Direction.OUTPUT
        self.led.value = False
        self.switch = digitalio.DigitalInOut(self.switchPin)
        self.switch.direction = digitalio.Direction.INPUT

    def isOn(self):
        return self.led.value

    def isSwitchOn(self):
        # prevent undefined state if the switch led is off, switch led must be on for the switch to work
        if self.led.value == False:
            return False
        return self.switch.value
    
    def setLed(self, value):
        self.led.value = value

    def getColor(self):
        return self.colour

    def getIndex(self):
        return self.index

    def getSwitchIndex(self):
        return self.indexSwitch
    