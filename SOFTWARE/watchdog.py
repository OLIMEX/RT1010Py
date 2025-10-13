from machine import WDT, Pin
from machine import reset_cause, PWRON_RESET, SOFT_RESET, WDT_RESET

# see details on
#    https://docs.micropython.org/en/latest/library/machine.html#machine-constants
RESET_CAUSE = { PWRON_RESET:'PWRON_RESET', SOFT_RESET:'SOFT_RESET', WDT_RESET:'WDT_RESET' }

rc = reset_cause()
print( "Reset cause: %i (%s)" % (rc, RESET_CAUSE[rc] ) )
print( "Set Watchdog to 5sec" )
print( "Press Boot1 to feed watchdog before" )
print( "  it resets the microcontroler" )

btn = Pin( Pin.board.BT1, Pin.IN ) # Boot1 button. 0=pressed, 1=released
dog = WDT( timeout=5000 ) # 5 sec before activation

def btn_press( btn ):
 global dog
 print( "Feed watchdog!" )
 dog.feed()

# Attach event to button
btn.irq( handler=btn_press, trigger=Pin.IRQ_FALLING )



