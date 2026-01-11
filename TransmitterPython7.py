
import pigpio
import time
import config

def ledTransmit(ledButton):
	
	#pi = pigpio.pi()
	#if not pi.connected:
	#	exit()
		
	transmitPin = 13;
	config.pi.set_mode(transmitPin, pigpio.OUTPUT)
	
	listLedButton = list(ledButton)
	
	reader = open("LedCodes.txt")
	
	while True:
	
		currentLine = reader.readline()
		
		equalButton = False
		
		buttonLength = len(listLedButton)
		
		for i in range(buttonLength):
			if listLedButton[i] != currentLine[i]:
				break
			
			if i == (len(listLedButton) - 1):
				equalButton = True
				
		
		if equalButton:
			binaryLed = currentLine[buttonLength+1:buttonLength+33]
			break
	
	
	reader.close()
	
	
	isTransmit = False #checks if the signal is transimitted
	
	#signal transmision	
	for i in range (5):
		
		t1 = time.perf_counter()
		
		

		config.pi.hardware_PWM(transmitPin, 38000, 500000)
		delayTime(9000)

		config.pi.hardware_PWM(transmitPin, 0, 0)
		delayTime(4500)

		for j in range (32):
			if binaryLed[j] == "0":
					config.pi.hardware_PWM(transmitPin, 38000, 500000)
					delayTime(563)
					config.pi.hardware_PWM(transmitPin, 0, 0)
					delayTime(563)
				
			else:					
					config.pi.hardware_PWM(transmitPin, 38000, 500000)
					delayTime(563)
					config.pi.hardware_PWM(transmitPin, 0, 0)
					delayTime(1688)


		config.pi.hardware_PWM(transmitPin, 38000, 500000);
		delayTime(563)
		config.pi.hardware_PWM(transmitPin, 0, 0);
		
		
		t2 = time.perf_counter()

		delayTime(100000) #200000 and 1000000 work well
		
		if (t2-t1)*1000 < 83:
			isTransmit = True


		print("DONE TRANSMITTING. Time in ms: ", (t2-t1)*1000) #note: total time in theory should be 68ms
		
		
		if i > 0 and isTransmit == True:
			break

	

	#pi.stop()
	
def delayTime(microSec):
	
	timeStop = time.perf_counter()*1000000 + microSec - 140 #-140 works well since the delay using python is not %100 accurate
	
	while time.perf_counter()*1000000 < timeStop:
		pass


#led_transmit("on")


