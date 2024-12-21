import digitalio

class LedNormal:
    pin = None
    colour = None
    led = None
    index = None

    def __init__(self, pin, colour, index):
        self.pin = pin
        self.colour = colour
        self.index = index
        self.led = digitalio.DigitalInOut(self.pin)
        self.led.direction = digitalio.Direction.OUTPUT
        self.led.value = False

    def isOn(self):
        return self.led.value
    
    def setLed(self, value):
        self.led.value = value

    def getColor(self):
        return self.colour

    def getIndex(self):
        return self.index
    