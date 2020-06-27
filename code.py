import time
import board
import pulseio
import touchio

led = pulseio.PWMOut( board.D13, frequency = 5000, duty_cycle = 128 )
led0 = pulseio.PWMOut( board.D0, frequency = 5000, duty_cycle = 128 )
led90 = pulseio.PWMOut( board.D2, frequency = 5000, duty_cycle = 128 )
led180 = pulseio.PWMOut( board.D3, frequency = 5000, duty_cycle = 128 )

touch = touchio.TouchIn( board.D4 )

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

        tmpduty = valduty << 8
        led.duty_cycle = tmpduty
        led0.duty_cycle = tmpduty
        led90.duty_cycle = tmpduty
        led180.duty_cycle = tmpduty

    # deal w/ switching modes
    #wason = switch.value
    wason = not touch.value
    time.sleep(0.005)  # 5ms delay
    #if not wason and not switch.value :
    if not wason and touch.value :
        # both was and is currently pressed, so toggle throbbing mode
        throbbing = not throbbing
        # wait until they release the button
        #while not switch.value :
        while touch.value :
            time.sleep(0.005)  # debounce 5ms delay
