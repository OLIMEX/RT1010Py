from machine import Pin
import time

led = Pin('GPIO_11', Pin.OUT) # create output pin on GPIO11

while 1 :
    led.on()                 # set pin to "on" (high) level
    time.sleep_ms(500)       # sleep for 500 milliseconds
    led.off()                # set pin to "off" (low) level
    time.sleep_ms(500)       # sleep for 500 milliseconds
    