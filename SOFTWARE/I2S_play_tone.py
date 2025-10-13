# Play a pure audio tone out of a speaker or headphones on the
# RT1010py from Olimex together with MAX98357A I2S
#
# - write audio samples containing a pure tone to an I2S amplifier or DAC module
# - tone will play continuously in a for loop (for few seconds)
#
# Blocking version
# - the write() method blocks until the entire sample buffer is written to I2S
#
# Based on micropython-i2s-examples from miketeachman
#   https://github.com/miketeachman/micropython-i2s-examples
#   The MIT License (MIT)
#   Copyright (c) 2022 Mike Teachman
#   https://opensource.org/licenses/MIT


import os
import math
import struct
from machine import I2S
from machine import Pin

def make_tone(rate, bits, frequency):
    # create a buffer containing the pure tone samples
    samples_per_cycle = rate // frequency
    sample_size_in_bytes = bits // 8
    samples = bytearray(samples_per_cycle * sample_size_in_bytes)
    volume_reduction_factor = 32
    range = pow(2, bits) // 2 // volume_reduction_factor
    
    if bits == 16:
        format = "<h"
    else:  # assume 32 bits
        format = "<l"
    
    for i in range(samples_per_cycle):
        sample = range + int((range - 1) * math.sin(2 * math.pi * i / samples_per_cycle))
        struct.pack_into(format, samples, i * sample_size_in_bytes, sample)
        
    return samples

# ======= AUDIO CONFIGURATION =======
TONE_FREQUENCY_IN_HZ = 440
SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO  # only MONO supported in this example
SAMPLE_RATE_IN_HZ = 22_050
# ======= AUDIO CONFIGURATION =======

BUFFER_LENGTH_IN_BYTES = 2000
audio_out = I2S( 3,
    sck=Pin.board.D10,
    ws=Pin.board.D9,
    sd=Pin.board.D11,
    mode=I2S.TX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

samples = make_tone(SAMPLE_RATE_IN_HZ, SAMPLE_SIZE_IN_BITS, TONE_FREQUENCY_IN_HZ)

# continuously write tone sample buffer to an I2S DAC
print("==========  START PLAYBACK ==========")
try:
    for i in range(1000):
        num_written = audio_out.write(samples)

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

# cleanup
audio_out.deinit()
print("Done")