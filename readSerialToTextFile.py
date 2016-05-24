"""
ReadLightAndTemp

This file reads data sent to serial port and writes the data to a text file
continuously.

"""

import os.path  # Import path method to direct to data file

import sys  # Import sys module

import time  # Import sleep method for delay

import serial  # Import module to read serial port

import cv2 # Import cv2 for image capture

import sqlite3 # Import sqlite3 for storing data to database

# Declare string variable for controller device file
device = "/dev/ttyACM0"
# Declare string variable for path to save file
savePath = "/home/sdharsee/Projects/ReadLightAndTempProject/Data/"

# Declare object for controller port, with baud rate 9600, and timeout of 9600
ser = serial.Serial(device, 9600, timeout=500)

# Declare path to data file directory
saveFile = savePath + time.strftime("%Y%m%d-%H%M%S")

imageSavePath = savePath + "/Images"    # Declare path to images folder

# If the directory where data and images should be saved do not exist, create them
if not os.path.exists(savePath):
    os.makedirs(savePath)   # Create data directory
    os.makedirs(imageSavePath)  # Create image directory
elif not os.path.exists(imageSavePath):
    os.makedirs(imageSavePath) # Create image directory

# Prompt for name of data file
saveFile = "LightAndTemp_" + time.strftime("%Y%m%d-%H%M%S")

# Declare path to save file
#dataFilePath = os.path.join(savePath, saveFile + ".txt")
#imageFilePath = os.path.join(savePath, imageSavePath)

databasePath = 'lightAndTempDatabase.db'
dataTable = 'lightAndTempDataTable'
databaseConn = sqlite3.connect(databasePath)
databaseCursor = databaseConn.cursor()

# Create data table if it does not exist
def create_table(data_Table):
    databaseCursor.execute('CREATE TABLE IF NOT EXISTS ' + data_Table + '(DateAndTime TEXT, Light_Value REAL, Temp_C FLOAT)')
    

# Enter data into data table in database
def data_entry(lightTempDataString, data_Table):
    executionString = "INSERT INTO " + data_Table + " VALUES("
    for i, item in enumerate(lightTempDataString[:-1]):
        item = lightTempDataString[i]
        executionString += str(item) + ', '
    executionString += lightTempDataString[-1]
    executionString += ')'
    databaseCursor.execute(executionString)
    ###databaseCursor.execute("INSERT INTO " + data_Table + " VALUES(" + lightTempDataString + ")")
    databaseConn.commit()
    

###cam = cv2.VideoCapture(1)  # Initialize web cam. 1 is the index for the web cam

create_table(dataTable)

# Loop to input data
while True:
    try:
        # Update currentDataPoint
        currentDataPoint = ser.readline().split()
        for i, item in enumerate(currentDataPoint):
            item = currentDataPoint[i].decode(encoding='utf-8')
            currentDataPoint[i] = item
        ###currentDataPoint[0], currentDataPoint[1] = currentDataPoint[0].decode(encoding='utf-8'), currentDataPoint[1].decode(encoding='utf-8')
        
        #Add DateAndTime to the beginning of the list
        currentDataPoint.reverse()
        currentDataPoint.append(time.strftime("%Y%m%d-%H%M%S"))
        currentDataPoint.reverse()
        
        ###rateAndTemp = ser.readline()   # Update value for light reading and temp reading
            
        ###imageName = currentDateTime + ".jpg" # Set image name to be currentDateTime
        
        # Placed cam variable declaration here before moving
        
        ###retval, image = cam.read()  # Read image from camera
        ###cv2.imwrite(imageSavePath + "/" + imageName, image)     #Save the image
        
        ###time.sleep(0.5)  # Delay for 0.5 second(s)
        
        # Store data into lightAndTempDatabase
        data_entry(currentDataPoint, dataTable)
        
    except KeyboardInterrupt:
        break

###del(cam)
databaseCursor.close()
databaseConn.close()
sys.exit()
