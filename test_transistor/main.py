import time
import board
import digitalio

t = digitalio.DigitalInOut(board.GP16)
t.direction = digitalio.Direction.OUTPUT

def press_power_button():
    t.value = True
    time.sleep(0.5)
    t.value = False

def turn_off_the_pc():
    t.value = True
    print("turning off pc")
    time.sleep(5)
    t.value = False
    print("done")
    
    
press_power_button()
#turn_off_the_pc()