# Play a WAV audio file out of a speaker or headphones
# RT1010py from Olimex together with MAX98357A I2S
#
# - read audio samples from a WAV file stored on internal flash memory
# - write audio samples to an I2S amplifier or DAC module
# - the WAV file will play once
#
# Blocking version
# - the write() method blocks until the entire sample buffer is written to I2S
#
# Use a tool to copy the WAV file "side-to-side-8k-16bits-stereo.wav"
#   to internal flash memory. The Thonny IDE also offers an easy way to copy
#   this file (View->Files, `Upload to /` option).
#
# Based on micropython-i2s-examples from miketeachman
#   https://github.com/miketeachman/micropython-i2s-examples
#   The MIT License (MIT)
#   Copyright (c) 2022 Mike Teachman
#   https://opensource.org/licenses/MIT
#
from machine import I2S, Pin

i2s = I2S(3, sck=Pin.board.D10, 
			ws=Pin.board.D9, 
			sd=Pin.board.D11, 
			mode=I2S.TX,
			bits=16, # WAV_SAMPLE_SIZE_IN_BITS
			format=I2S.STEREO,
			rate=8000, # WAV_SAMPLE_SIZE_IN_BITS 
			ibuf=5000 )

wav = open("side-to-side-8k-16bits-stereo.wav", "rb")
pos = wav.seek(44)  # advance to first byte of Data section in WAV file

# allocate sample array
# memoryview used to reduce heap allocation
wav_samples = bytearray(1000)
wav_samples_mv = memoryview(wav_samples)

# continuously read audio samples from the WAV file
# and write them to an I2S DAC
print("==========  START PLAYBACK ==========")
while True:
    num_read = wav.readinto(wav_samples_mv)
    # end of WAV file?
    if num_read == 0:
        # end-of-file, exxit reading loop.
        break
    # PLay the buffer
    _ = i2s.write(wav_samples_mv[:num_read])

# cleanup
wav.close()
i2s.deinit()
print("Done")
