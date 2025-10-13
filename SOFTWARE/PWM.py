# Pulse a LED wired on pin D1
import time
from machine import Pin, PWM

pwm = PWM(Pin('D1'))
pwm.freq(1000)

duty = 0
direction = 1
for x in range(8 * 256):
	duty += direction
	if duty > 255:
		duty = 255
		direction = -1
	elif duty < 0:
		duty = 0
		direction = 1
	pwm.duty_u16(duty * duty)
	time.sleep(0.001)
