# Store data in the i.MX RT1010py PMIC SNVS_LPGPR registers.
# 128 bits/16 bytes organized in 4x 32 bits register.
#
# SNVS_LPGPR registers do survive the ON/OFF PMIC cycle.
#
# This script is only made for demonstration purpose.
# See IMXRT1010RM.pdf Processor reference manual @ 2.6.15

#
from micropython import const
from machine import mem32, RTC
import struct

def pretty_bin32( val ):
    # Just make user friendly 32 bit values
    _parts = ('%08s' % bin((val & 0xFF000000)>>24).replace('0b','') ,
              '%8s' % bin((val & 0x00FF0000)>>16).replace('0b','') ,
              '%8s' % bin((val & 0x0000FF00)>>8 ).replace('0b','') ,
              '%8s' % bin((val & 0x000000FF)    ).replace('0b','') )
    return ' : '.join( _s.replace(' ','0') for _s in _parts )

SNVS_BASE = const( 0x400D_4000 )

def LPGPR_addr( index ):
    assert 0<=index<=3
    return SNVS_BASE+0x100+(index*0x04)

def LPGPR_get( index ):
    # return the LPGPR register content as a buffer of 4 bytes
    addr = LPGPR_addr( index )
    return struct.pack('>I',mem32[addr])

def LPGPR_set( index, buffer ):
    # Set a LPGPR register with the data (4 bytes) stored in the buffer
    assert len(buffer)==4, "Buffer must have 4 bytes"
    addr = LPGPR_addr( index )
    mem32[addr] = struct.unpack( '>I', buffer )[0]

# Store the Day,Month,Hour,Sec in the LPGPR[0]
rtc = RTC()
_year, _month, _day, _dow, _hour,_min, _sec, _ms = rtc.datetime()
data = bytes([_day, _month, _hour, _min])
print( "Encode %i/%i %i:%i" % (_day, _month, _hour, _min) )
print(  data, "=> LPGPR[0]")
LPGPR_set( 0, data )
print()

# Store 12 bytes message into remaining storage
sMessage = "OlimexRT1010"
data = sMessage.encode("ASCII")
print( "Encode message %s" % sMessage )
print( data, "=> LPGPR[1..3]" )
LPGPR_set( 1, data[0:4] )
LPGPR_set( 2, data[4:8] )
LPGPR_set( 3, data[8:12] )
LPGPR_set( 3, data[8:12] )
print()

print( "Now you can inspect the content with pmic_gpr_get.py script!" )
print( "Register will survive the On/OFF cycle" )


