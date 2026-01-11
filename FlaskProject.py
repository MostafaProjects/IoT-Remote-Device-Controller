
from flask import Flask, render_template, request
#from blinkPython import blink_code
from TransmitterPython7 import ledTransmit
from SQLTempHumid import getTrials, getMeasurements, insertTrial, insertManyMeasurements
import sqlite3
import pigpio
import threading
import time
import config
import datetime

import board #this is for the temp and humidiy sensor
import adafruit_dht #this is for the temp and humidiy sensor

app = Flask(__name__)

#variable for temp/humidity
dhtDevice = adafruit_dht.DHT11(board.D17)

temperature = 0
humidity = 0

isStart = True #variable to choose between the test.html and testingRunning.html
stopThread2Event = threading.Event()
measurementList = [] #this will hold a list of tuples for the measurements in runTrial()
completeDate = ""
trialNumber = 0
#t2 = None

#calculated the temperatue and humidity levels
def getTempHumid():
	
	#gets the results and returns it if successulf
	while True:
		
		try:
			global temperature #need to declare as global since it modifies the "temperature" variable declared above
			temperature = dhtDevice.temperature
			global humidity #same as temperture variable logic
			humidity = dhtDevice.humidity

			break
			
		except RuntimeError as error:
			print(error.args[0])
			time.sleep(2)
			continue
			
	
#checks if the light level changes in the room and turns the led on/off based on the level. Also checks for temperature and humidity every 30 seconds
def roomCheck():
	
	#storing the result from opening the i2c communication on the ADC7830 component that is connected to the light sensor
	handle = config.pi.i2c_open(1, 0x4b) 
	
	lightOn = False
	timeElapsed = 0
	
	while True:
		data = config.pi.i2c_read_word_data(handle, 0)

		#if the light level is > 50000 this means that the room is dark and turns on the led, if < 40000 it means the room has enough light and turns off led
		if(data > 50000 and lightOn == False):
			lightOn = True
			led_transmit("on")
		elif(data < 40000 and lightOn == True):
			lightOn = False
			led_transmit("off")
		
		time.sleep(5)
		timeElapsed += 5
		
		#calculated the temperature and humididty levels every 30 seconds
		if timeElapsed == 30:
			getTempHumid()
			print(temperature, humidity)
			timeElapsed = 0
		
def runTrial():
	global measurementList
	measurementList = []
	
	global completeDate
	global trialNumber
	
	while True:
			
		currentTime = datetime.datetime.now()
		year = currentTime.strftime("%Y")
		month = currentTime.strftime("%m")
		day = currentTime.strftime("%d")
		completeDate = day + "-" + month + "-" + year
		
		while stopThread2Event.is_set():
			getTempHumid()
			
			currentTime = datetime.datetime.now()
			
			hours = currentTime.strftime("%H")
			minutes = currentTime.strftime("%M")
			seconds = currentTime.strftime("%S")
			
			measurement = (hours, minutes, seconds, temperature, humidity, trialNumber)
			measurementList.append(measurement)
			
			
			print(temperature, humidity)
			time.sleep(10)

		#pausing the thread until starting another test trial and clearing previous results
		stopThread2Event.wait()
		measurementList = []
		
	

#create some routes
@app.route("/")
def index():
	getTempHumid()
	
	return render_template('home.html', temp = temperature, humid = humidity)
	
@app.route("/home")
def led():
	nameURL = request.args.get('led')
	print(nameURL)
	
	ledTransmit(nameURL)
	
	return render_template('home.html', temp = temperature, humid = humidity)
	
@app.route("/testing")
def testing():
	
	nameURL = request.args.get('testing')
	
	#return the list of trials to display
	trials = getTrials()
	
	global isStart, t2, stopThread2Event
	htmlTemplate = 'testing.html'
	
	if nameURL == "stop":
		isStart = False
		
		#checks if the thread is alive and stop the thread if so
		if t2.is_alive():
			stopThread2Event.clear()
			#t2.join()

			global measurementList
			global completeDate
			
			description = input("Enter the description of the Trial: ")
			
			insertTrial(completeDate, description)
			insertManyMeasurements(measurementList)
			
			#update Trials table when pressing the stop button
			trials = getTrials()
			
		
	elif nameURL == "start":
		htmlTemplate = 'testingRunning.html'
		isStart = True
		
		global trialNumber
		trialNumber = len(trials) + 1
		
		#start the thread and record results
		stopThread2Event.set()
		
		if not t2.is_alive():
			t2.start()
	
	
	return render_template(htmlTemplate, trials = trials)

@app.route("/testing/measurements")
def measurements():
	
	#retrieving which trial number the user selects and parsing it to int
	nameURL = request.args.get('testing')
	measurementNumber = int(nameURL)
	
	#fetching the measurments logs based on the trial number selected
	measurements = getMeasurements(measurementNumber)
	
	temp = []
	humid = []
	
	tempAverage = 0
	humidAverage = 0
	
	#storing all the tempereature and humidity results in a list
	for i in range(len(measurements)):
		temp.append(measurements[i][4])
		humid.append(measurements[i][5])
		
		tempAverage += measurements[i][4]
		humidAverage += measurements[i][5]
		

	#calculating the max, min and average for both
	tempMax = max(temp)
	tempMin = min(temp)
	tempAverage = round(tempAverage/len(temp), 2)
	
	humidMax = max(humid)
	humidMin = min(humid)
	humidAverage = round(humidAverage/len(humid), 2)
	
	
	summaryResults = [tempMax, tempMin, tempAverage, humidMax, humidMin, humidAverage]
		
	return render_template('measurements.html', measurements = measurements, summaryResults = summaryResults)
	

t1 = threading.Thread(target=roomCheck)
t1.start()
t2 = threading.Thread(target=runTrial)


app.run(host="0.0.0.0")


