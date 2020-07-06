import time
import board
import pulseio
import touchio
import adafruit_ws2801
import adafruit_fancyled.adafruit_fancyled as fancy

led = pulseio.PWMOut( board.D13, frequency = 5000, duty_cycle = 128 )
led0 = pulseio.PWMOut( board.D0, frequency = 5000, duty_cycle = 128 )

strip = adafruit_ws2801.WS2801( board.D3, board.D4, 7, auto_write=False)

touch = touchio.TouchIn( board.A0 )

throbbing = True
goingup = True
valduty = 5
wason = False

# across the rainbow
grad = [ (0.0,0xFF0000), (0.33,0x00FF00), (0.67,0x0000FF), (1.0,0xFF0000) ]
palette = fancy.expand_gradient( grad, 20 )

offset = 0.25
color = fancy.palette_lookup( palette, offset )
strip.fill( color.pack() )
#strip.fill( 0xFF0000 )
strip.show()

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
        offset = ( valduty % 256 ) / 255
        color = fancy.palette_lookup( palette, offset )
        strip.fill( color.pack() )
        strip.show()

    # deal w/ switching modes
    wason = not touch.value
    time.sleep(0.005)  # 5ms delay

    if not wason and touch.value :
        # both was and is currently pressed, so toggle throbbing mode
        throbbing = not throbbing
        # wait until they release the button
        while touch.value :
            time.sleep(0.005)  # debounce 5ms delay