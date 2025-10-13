# A bipolar push button can be used to control the "ON" signal
# as well as an input pin (eg: D0) attached to an IRQ fired by
# the same button controling the "ON" signal.
from machine import Pin

def power_off_cb( obj ):
    print( "Power off pressed" )
    
# Check doc for more details on parameters
# https://docs.micropython.org/en/latest/library/machine.Pin.html
poff = Pin( Pin.board.D0, Pin.IN, Pin.PULL_UP )
poff.irq( handler=power_off_cb, trigger=Pin.IRQ_FALLING, hard=True )
