# Change the i.MX RT1010 PMIC BTN_PRESS_TIME from 5s to 10s.
# This update the configuration in LPRC register (not permanent update)
#
# See IMXRT1010RM.pdf Processor reference manual @ 2.6.11.1
#
# This script is only made for demonstration purpose
#
from micropython import const
from machine import mem32

def pretty_bin32( val ):
    # Just make user friendly 32 bit values
    _parts = ('%08s' % bin((val & 0xFF000000)>>24).replace('0b','') ,
              '%8s' % bin((val & 0x00FF0000)>>16).replace('0b','') ,
              '%8s' % bin((val & 0x0000FF00)>>8 ).replace('0b','') ,
              '%8s' % bin((val & 0x000000FF)    ).replace('0b','') )
    return ' : '.join( _s.replace(' ','0') for _s in _parts )


def get_bits( reg_value, start_bit, bit_len=1 ):
    # return the value of bits starting at position start_bit (0..31)
    # and for a given bit length from a binary encoded value (val)
    _mask = (2**bit_len)-1 # 0b1, 0b11, 0b111, ...
    _mask = _mask << start_bit
    return (reg_value & _mask)>>start_bit

def set_bits( reg_value, reg_bits, start_bit, bit_len, value ):
    # Update the register value (reg_value) encoded over reg_bits (eg:32).
    # set the value (value) from the start_bit (lowest bit) over bit_len bits.
    assert reg_bits in (8,16,24,32), "Invalid bits number"
    _mask = (2**bit_len)-1 # 0b1, 0b11, 0b111, ...
    _mask = _mask << start_bit
    # Invert the mask
    _filter = 0xFF
    for i in range( (reg_bits//8)-1 ):
        _filter = (_filter<<8) + 0xFF
    _filter = _filter ^ _mask
    # filter the reg_value
    reg_value = reg_value & _filter
    # Insert the new value into the filtered reg_value
    return reg_value | (value<<start_bit)
        
    

SNVS_BASE = const( 0x400D_4000 )
SNVS_LPCR    = const( SNVS_BASE + 0x38 ) # SNVS_LP Control Register

ON_TIME_500ms = const( 0 )
ON_TIME_50ms  = const( 1 )
ON_TIME_100ms = const( 2 )
ON_TIME_0ms   = const( 3 )
DEBOUNCE_50ms = const( 0 )
DEBOUNCE_100ms= const( 1 )
DEBOUNCE_500ms= const( 2 )
DEBOUNCE_0ms  = const( 3 )
BTN_PRESS_5s  = const( 0 )
BTN_PRESS_10s = const( 1 )
BTN_PRESS_15s = const( 2 )
BTN_PRESS_DISABLED =  const( 3 )
ON_TIME_TEXT = {ON_TIME_500ms:'500ms', ON_TIME_50ms:'50 ms', ON_TIME_100ms: '100ms', ON_TIME_0ms:'0ms'}
DEBOUNCE_TEXT = {DEBOUNCE_50ms:'50ms', DEBOUNCE_100ms:'100 ms', DEBOUNCE_500ms: '500ms', DEBOUNCE_0ms:'0ms'}
BTN_PRESS_TIME_TEXT = {BTN_PRESS_5s:'5s', BTN_PRESS_10s:'10s', BTN_PRESS_15s:'15s', BTN_PRESS_DISABLED:'disabled'}


# Get 32bits register values
lpcr_value = mem32[ SNVS_LPCR ]
# IMXRT1010RM.pdf Processor reference manual @ 2.6.11
on_time = get_bits( lpcr_value, 20, 2 )
debounce = get_bits( lpcr_value, 18, 2 )
btn_press_time = get_bits( lpcr_value, 16, 2)

# IMXRT1010RM.pdf Processor reference manual @ 2.6.11
print( '--- Original Config -------------------------------' )
print( 'LPRC register :', pretty_bin32(lpcr_value) )
print( 'LPRC On-time  : %s (%s)' % (ON_TIME_TEXT[on_time],bin(on_time)) )
print( 'LPRC Debounce : %s (%s)' % (DEBOUNCE_TEXT[debounce],bin(debounce)) )
print( 'LPRC Btn_Press_time : %s (%s)' % (BTN_PRESS_TIME_TEXT[btn_press_time],bin(btn_press_time)) )
print()

# Change the configuration
#   lpcr_value is a 32bits value
#   Change on bit 16 (over 2 bit long)
#   Set the BTN_PRESS_10s value
lpcr_value = set_bits( lpcr_value, 32, 16, 2, BTN_PRESS_10s )
mem32[ SNVS_LPCR ] = lpcr_value


# Reread the value from register
new_lpcr_value = mem32[SNVS_LPCR]
on_time = get_bits( new_lpcr_value, 20, 2 )
debounce = get_bits( new_lpcr_value, 18, 2 )
btn_press_time = get_bits( new_lpcr_value, 16, 2)

print( '--- Updated Config -------------------------------' )
print( 'LPRC register :', pretty_bin32(lpcr_value) )
print( 'LPRC On-time  : %s (%s)' % (ON_TIME_TEXT[on_time],bin(on_time)) )
print( 'LPRC Debounce : %s (%s)' % (DEBOUNCE_TEXT[debounce],bin(debounce)) )
print( 'LPRC Btn_Press_time : %s (%s)' % (BTN_PRESS_TIME_TEXT[btn_press_time],bin(btn_press_time)) )
print()
