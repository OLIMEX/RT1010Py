# This script show the Pin.board.x with its corresponding Pin.cpu.y
#
from machine import Pin

board_pins = "A0,A1,A2,A3,A4,BT0,BT1,CS0,D0,D1,D10,D11,D12,D13,D14,D2,D3,D4,D5,D6,D7,D8,D9,LED,MCK,RELAY1,RELAY2,RX,SCK,SCK_RX,SCK_TX,SCL1,SCL2,SDA1,SDA2,SDI,SDO,SD_RX,SD_TX,TX,USB_OTG1_PWR,WS_RX,WS_TX"
for pin_name in board_pins.split(','):
 s = "%r" % eval( "Pin.board.%s" % pin_name ) # Returns "Pin(xxxx)"
 print( "Pin.board.%s => Pin.cpu.%s" % (pin_name, s.replace("Pin(","").replace(")","") ))

