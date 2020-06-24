import time
import board
import pulseio
from digitalio import DigitalInOut, Direction, Pull
 
# For Gemma M0, Trinket M0, Metro M0 Express, ItsyBitsy M0 Express, Itsy M4 Express
switch = DigitalInOut(board.D2)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

led = pulseio.PWMOut( board.D13, frequency = 5000, duty_cycle = 128 )

throbbing = True
goingup = True
valduty = 5

while True :
    if throbbing :
        if goingup :
            valduty = valduty + 1
            if valduty > 250 :
                goingup = False
        else :
            valduty = valduty - 1
            if valduty < 5 :
                goingup = True
        led.duty_cycle = valduty << 8

    # deal w/ switching modes
    wason = switch.value
    time.sleep(0.005)  # debounce 5ms delay
    if not wason and not switch.value :
        # both was and is currently pressed, so toggle throbbing mode
        throbbing = not throbbing
        # wait until they release the button
        while not switch.value :
            time.sleep(0.005)  # debounce 5ms delay
