import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from displayio import I2CDisplay as I2CDisplayBus

# https://docs.circuitpython.org/projects/displayio_ssd1306/en/latest/examples.html

class Display:
    # Constants for display dimensions
    WIDTH = 128
    HEIGHT = 32  # Change to 64 if needed
    splash = None
    display = None

    fontHeight = terminalio.FONT.get_bounding_box()[0]
    #fontWidth = terminalio.FONT.get_bounding_box()[1]
    # width seems to be a bit big on my display
    fontWidth = terminalio.FONT.get_bounding_box()[0]

    def __init__(self):
        # Release any previously used displays
        displayio.release_displays()

        # Set up I2C using busio
        i2c = busio.I2C(board.GP5, board.GP4)  # GP5 for SCL and GP4 for SDA
        display_bus = I2CDisplayBus(i2c, device_address=0x3C)

        # Create the display object
        self.display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=self.WIDTH, height=self.HEIGHT)

        #print(dir(self.display))

        # Make the display context
        self.splash = displayio.Group()
        self.display.root_group = self.splash
        self.display.auto_refresh = False
        self.display.brightness = 0
        self.display.refresh()

    def clear(self):
        while len(self.splash) > 0:
            self.splash.pop()
            self.display.refresh()
        

    def printText(self, text, position = "centre", index = 0, xPosition = "centre" ):
        text_area = None
        y = self.HEIGHT // 2 - 1
        if position == "top":
            y = self.fontHeight
        elif position == "bottom":
            y = self.HEIGHT - self.fontHeight

        x = 28
        if xPosition == "centre":
            x = (self.WIDTH // 2) - ((len(text) * self.fontWidth) // 2)
        elif xPosition == "left":
            x = self.fontWidth

        if index < len(self.splash):
            text_area = self.splash[index]
        else:
            # self.clear() clear outside of this
            # Create a text label
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=x, y=y)
            # Add the text label to the display group
            self.splash.append(text_area)

        text_area.text = text
        text_area.x = x
        text_area.y = y

        self.display.refresh()

    def animateText(self, text, frame, frame_count, position = "centre", index = 0):
        text_area = None
        y = self.HEIGHT // 2 - 1
        if position == "top":
            y = self.fontHeight
        elif position == "bottom":
            y = self.HEIGHT - self.fontHeight

        if index < len(self.splash):
            text_area = self.splash[index]
        else:
            # self.clear() clear outside of this
            # Create a text label
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=y)
            # Add the text label to the display group
            self.splash.append(text_area)
        
        
        # Get the width of the display and the text
        display_width = self.display.width
        text_width = text_area.bounding_box[2]
        
        offset = (frame * (text_width + display_width) // frame_count) - text_width
            
        # Update the position of the text
        text_area.x = offset
            
        # Update the display
        #self.display.refresh()
