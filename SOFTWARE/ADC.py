import time
from machine import ADC,Pin

adc = ADC(Pin.board.A0) # can also use ADC("A0")
while True:
 value = adc.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
 volts = 3.3 * value / 65535
 print( value, "=", volts )
 time.sleep( 0.5 )
