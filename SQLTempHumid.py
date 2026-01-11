
import sqlite3


#initialize DB
def getConnection():
	try:
		return sqlite3.connect("tempHumid.db")
		
	except Exception as e:
		print(f"Error: {e}")
		raise
		

#create a table to store temperature and humidity readings 
def createTables(connection):
	
	query1 = """
	CREATE TABLE IF NOT EXISTS Trials (
		trial_id INTEGER PRIMARY KEY,
		date TEXT NOT NULL,
		description TEXT
	)
	"""
	
	query2 = """
	CREATE TABLE IF NOT EXISTS Measurements (
		entry_id INTEGER PRIMARY KEY,
		hours int NOT NULL,
		minutes int NOT NULL,
		seconds int NOT NULL,
		temperature DECIMAL(3, 2) NOT NULL,
		humididty int NOT NULL,
		trial_id int,
		FOREIGN KEY (trial_id) REFERENCES Trials(trial_id)
	)
	"""
	
	try:
		with connection:
			connection.execute(query1)
			connection.execute(query2)
		
	except Exception as e:
		print(e)
			

def getTrials():
	
	connection = getConnection()
	connection.execute("PRAGMA foreign_keys = ON")
	
	
	query = "SELECT * FROM Trials"
	
	try:
		with connection:
			trials = connection.execute(query).fetchall()
			
			return trials
	
	except Exception as e:
		print(e)
		
def getMeasurements(trialNumber):
	
	connection = getConnection()
	connection.execute("PRAGMA foreign_keys = ON")
	
	
	query = "SELECT * FROM Measurements WHERE trial_id = ?"
	
	try:
		with connection:
			measurements = connection.execute(query, (trialNumber,)).fetchall()
			return measurements
	
	except Exception as e:
		print(e)
	

def insertTrial(date, description):
	
	connection = getConnection()
	connection.execute("PRAGMA foreign_keys = ON")
	
	
	query = "INSERT INTO Trials (date, description) VALUES (?, ?)"
	
	try:
		with connection:
			connection.execute(query, (date, description))
			connection.commit()
	
	except Exception as e:
		print(e)
	
def insertManyMeasurements(measurements):
	
	connection = getConnection()
	connection.execute("PRAGMA foreign_keys = ON")
	
	
	query = "INSERT INTO Measurements (hours, minutes, seconds, temperature, humididty, trial_id) VALUES (?, ?, ?, ?, ?, ?)"
	
	try:
		with connection:
			connection.executemany(query, measurements)
			connection.commit()
	
	except Exception as e:
		print(e)
		
def deelte():
	
	connection = getConnection()
	#connection.execute("PRAGMA foreign_keys = ON")
	
	
	query = "DELETE FROM Trials WHERE trial_id > ?"
	
	try:
		with connection:
			connection.execute(query, (-1,))
			connection.commit()
	
	except Exception as e:
		print(e)

#main code below
'''
connection = getConnection()
connection.execute("PRAGMA foreign_keys = ON")

createTables(connection)

rows = getTrials(connection)

for row in rows:
	print(row)


connection.commit()
connection.close()

'''



'''
cursor = connection.cursor()

#test
cursor.execute("INSERT INTO Trials (date, description) VALUES (?, ?)", ("1-05-2026", "This is a test"))

for row in cursor.execute("SELECT * FROM Trials").fetchall():
	print(row)

#cursor.execute("DELETE FROM Trials WHERE trial_id > ?", (2,))



cursor.execute("INSERT INTO Readings (hours, minutes, seconds, trial_id) VALUES (?, ?, ? ,?)", (1, 2, 3, 2))

for row in cursor.execute("SELECT * FROM Readings").fetchall():
	print(row)

'''

'''
query2 = """
	CREATE TABLE IF NOT EXISTS Readings (
		entry_id INTEGER PRIMARY KEY,
		hours int NOT NULL,
		minutes int NOT NULL,
		seconds int NOT NULL,
		trial_id int,
		FOREIGN KEY (trial_id) REFERENCES Trials(trial_id)
	)
	"""

'''
