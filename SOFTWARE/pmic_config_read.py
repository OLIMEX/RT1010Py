# Read the i.MX RT1010 PMIC config in LPRC (and other) register
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

def get_bits( val, start_bit, bit_len=1 ):
    # return the value of bits starting at position start_bit (0..31)
    # and for a given bit length from a binary encoded value (val)
    _mask = (2**bit_len)-1 # 0b1, 0b11, 0b111, ...
    _mask = _mask << start_bit
    return (val & _mask)>>start_bit
    

SNVS_BASE = const( 0x400D_4000 )
SNVS_HPCOMR  = const( SNVS_BASE + 0x4 )  # SNVS_HP Command Register
SNVS_HPSR    = const( SNVS_BASE + 0x14 ) # SNVS_HP Status Register
SNVS_HPRTCMR = const( SNVS_BASE + 0x24 ) # SNVS_HP Real Time Counter MSB Register
SNVS_HPRTCLR = const( SNVS_BASE + 0x28 ) # SNVS_HP Real Time Counter LSB Register
SNVS_LPCR    = const( SNVS_BASE + 0x38 ) # SNVS_LP Control Register
SNVS_LPSR    = const( SNVS_BASE + 0x4C ) # SNVS_LP Status  Register
SNVS_LPSMCMR = const( SNVS_BASE + 0x5C ) # SNVS_LP Secure Monotonic Counter MSB Register
SNVS_LPSMCLR = const( SNVS_BASE + 0x60 ) # SNVS_LP Secure Monotonic Counter LSB Register
SNVS_HPVIDR1 = const( SNVS_BASE + 0xBF8 ) # SNVS_HP Version ID Register 1
SNVS_HPVIDR2 = const( SNVS_BASE + 0xBFC ) # SNVS_HP Version ID Register 2

# Get 32bits register values
hpcomr_value = mem32[ SNVS_HPCOMR ]
hpsr_value = mem32[ SNVS_HPSR ] 
hprtcmr_value = mem32[ SNVS_HPRTCMR ] # Must be configured properly before usage
hprtclr_value = mem32[ SNVS_HPRTCLR ]
lpcr_value = mem32[ SNVS_LPCR ]
lpsr_value = mem32[ SNVS_LPSR ]
# lpsmcmr_value = mem32[ SNVS_LPSMCMR ] # must be configured properly before usage
# lpsmclr_value = mem32[ SNVS_LPSMCLR ]
hpvidr1_value = mem32[ SNVS_HPVIDR1 ]
hpvidr2_value = mem32[ SNVS_HPVIDR2 ]

# ---- SNVS HP Command -----------------------------------
# IMXRT1010RM.pdf Processor reference manual @ 2.6.3
print( 'HP Command Register :', pretty_bin32(hpcomr_value) ) 
print( 'Non-privileged Access Allowed:', bool(get_bits(hpcomr_value,31,1)) )
print( 'LP Soft Reset disable :', bool(get_bits(hpcomr_value,5,1)) )
print( 'LP Soft Reset         :', bool(get_bits(hpcomr_value,4,1)) )
print()

# ---- SNVS HP ID & Version ------------------------------
# IMXRT1010RM.pdf Processor reference manual @ 2.6.18
print( 'HP Version ID Register 1:', pretty_bin32( hpvidr1_value ) )
print( 'HP Version ID Register 2:', pretty_bin32( hpvidr2_value ) )

print( 'Module ID            :', get_bits( hpvidr1_value, 16, 16) )
print( 'Major version        :', get_bits( hpvidr1_value, 8, 8) )
print( 'Minor version        :', get_bits( hpvidr1_value, 0, 8) )
print( 'Integration Options  :', get_bits( hpvidr2_value, 16, 8) )
print( 'ECO revision         :', get_bits( hpvidr2_value, 8, 8) )
print( 'Configuration options:', get_bits( hpvidr2_value, 0, 8) )
print()

# ---- HP Status ------------------------------------------
# IMXRT1010RM.pdf Processor reference manual @ 2.6.5
print( 'HPSR Register :', pretty_bin32(hpsr_value) )
bi = get_bits( hpsr_value, 7, 1 )
btn = get_bits( hpsr_value, 6, 1 )
lpdis = get_bits( hpsr_value, 4, 1 )
pi = get_bits( hpsr_value, 1, 1 )
hpta = get_bits( hpsr_value, 0, 1 )
print( 'HPSR Button Interrupt  :', bool(bi) )
print( 'HPSR Btn               :', bool(btn) )
print( 'HPSR Low Power Disable :', bool(lpdis) )
print( 'HPSR Periodic Interrupt:', bool(pi) ) # Periodic interrupt occured since last cleared
print( 'HPSR Time Alarm        :', bool(hpta) ) # HP Time Alarm occured since last cleared
print()

# ---- Display LPCR ---------------------------------------
# IMXRT1010RM.pdf Processor reference manual @ 2.6.11
print( 'LPRC register :', pretty_bin32(lpcr_value) )

on_time = get_bits( lpcr_value, 20, 2 )
debounce = get_bits( lpcr_value, 18, 2 )
btn_press_time = get_bits( lpcr_value, 16, 2)

ON_TIME_TEXT = {0:'500ms', 1:'50 ms', 2: '100ms', 3:'0ms'}
DEBOUNCE_TEXT = {0:'50ms', 1:'100 ms', 2: '500ms', 3:'0ms'}
BTN_PRESS_TIME_TEXT = {0:'5s', 1:'10s', 2:'15s', 3:'disabled'}

print( 'LPRC On-time : %s (%s)' % (ON_TIME_TEXT[on_time],bin(on_time)) )
print( 'LPRC Debounce : %s (%s)' % (DEBOUNCE_TEXT[debounce],bin(debounce)) )
print( 'LPRC Btn_Press_time : %s (%s)' % (BTN_PRESS_TIME_TEXT[btn_press_time],bin(btn_press_time)) )
print()

# ---- Display LPSR ---------------------------------------
#  IMXRT1010RM.pdf Processor reference manual @  20.6.12.4
print( 'LPSR register :', pretty_bin32(lpsr_value) )
set_power_off = get_bits( lpsr_value, 18 ) # Set Power-Off detected (btn pressed longuer that debounce)
emergency_off = get_bits( lpsr_value, 17 ) # Power-Off requested

print( 'LPSR Set Power Off :', bool(set_power_off) )
print( 'LPSR emergency Off :', bool(emergency_off) )
print()

# ---- Display RTCxx -------------------------------------
#  IMXRT1010RM.pdf Processor reference manual @  20.6.6
print( 'HPRTCMR SNVS_HP Real Time Counter' )
print( 'HPRTCMR Counter MSB :', pretty_bin32(hprtcmr_value) )
print( 'HPRTCMR Counter LSB :', pretty_bin32(hprtclr_value) )
