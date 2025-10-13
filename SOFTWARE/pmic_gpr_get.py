# Change the i.MX RT1010 PMIC SNVS_LPGPR to store data up to
# 16 bytes (or 4x 32 bits)
# 
#
# See IMXRT1010RM.pdf Processor reference manual @ 2.6.15
#
# This script is only made for demonstration purpose
#
from micropython import const
from machine import mem32
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

def LPGPR_as_int( index ):
    addr = LPGPR_addr( index )
    return mem32[addr]

def LPGPR_get( index ):
    # return the LPGPR register content as a buffer of 4 bytes
    addr = LPGPR_addr( index )
    return struct.pack('>I',mem32[addr])

def LPGPR_set( index, buffer ):
    # Set a LPGPR register with the data (4 bytes) stored in the buffer
    assert len(buffer)==4, "Buffer must have 4 bytes"
    addr = LPGPR_add( index )
    mem32[addr] = struct.unpack( '>I', buffer )[0]

# Display the content as raw content
print( "--- RAW -------------------------------------------" )
for i in range(4):
    data = LPGPR_get( i )
    print( "LPGPR[%i] :" % i, data )
    
print( "--- Binary ----------------------------------------" )
for i in range(4):
    value = LPGPR_as_int( i ) # Get the value as u32int
    print( "LPGPR[%i] :" % i, pretty_bin32(value) )
    
print( "--- Bytes -----------------------------------------" )
for i in range(4):
    value = LPGPR_get( i ) # Get the value as u32int
    print( "LPGPR[%i] :" % i, ", ".join( "%i" % _ for _ in value ) )
