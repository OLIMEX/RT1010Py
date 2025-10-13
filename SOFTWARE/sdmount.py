# Minimalist code for Mounting the RT1010py SDCard under /sd MicroPython filesystem folder
#
# Requires the sdcard.py file available from official micropython-lib
# https://github.com/micropython/micropython-lib/micropython/drivers/storage/sdcard
#
from machine import SPI, Pin
from sdcard import SDCard
import gc, os

sd_spi = SPI(2,baudrate=20_000_000)
sd_cs = Pin( Pin.cpu.GPIO_AD_01, Pin.OUT, value=1 )
sd = SDCard( sd_spi, sd_cs )
print("Mounting SDcard to /sd" )
sd_vfs = os.VfsFat(sd)
os.mount(sd_vfs, "/sd")

print("List /sd files")
print(os.listdir("/sd"))

# Use  os.umount('/sd')  to unmount the folder