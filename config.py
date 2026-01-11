
import pigpio
pi = pigpio.pi()
if not pi.connected:
		exit()
