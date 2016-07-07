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

from configparser import ConfigParser # Import configparser to read config file

import ast # Import ast to read string as dictionary

import serial_device # Import serial_device class

#Read config file to get settings for the device
cfg = ConfigParser()
cfg.read('readDataConf.ini')

# Declare string variable for controller device file
###device = "/dev/ttyACM0"
device = cfg.get('device_1', 'device')

# Declare device name
###name = "photonTest"
name = cfg.get('device_1', 'name')

# Declare device location
###location = "HomeDesktop"
location = cfg.get('device_1', 'location')

# Declare data fields as a dictionary [Field name: Field type]
###dataFields = {'DateAndTime' : 'TEXT', 'Light_Value' : 'REAL', 'Temp_C' : 'FLOAT'}
dataFieldsString = cfg.get('device_1', 'dataFields')
dataFields = ast.literal_eval(dataFieldsString)

# Declare string variable for path to save file
###savePath = "/home/sdharsee/Projects/ReadLightAndTempProject/Data/"

# Declare object for controller port, with baud rate 9600, and timeout of 9600
###databasePath = 'lightAndTempDatabase.db'
databasePath = cfg.get('device_1', 'databasePath')

# Declare object for controller device
controller = serial_device.DataDevice(device, name, location, dataFields, databasePath)

###imageSavePath = savePath + "/Images"    # Declare path to images folder

# If the directory where data and images should be saved do not exist, create them
###if not os.path.exists(savePath):
###    os.makedirs(savePath)   # Create data directory
###    os.makedirs(imageSavePath)  # Create image directory
###elif not os.path.exists(imageSavePath):
###    os.makedirs(imageSavePath) # Create image directory

# Prompt for name of data file
###saveFile = "LightAndTemp_" + time.strftime("%Y%m%d-%H%M%S")

# Declare path to save file
###imageFilePath = os.path.join(savePath, imageSavePath)

###cam = cv2.VideoCapture(1)  # Initialize web cam. 1 is the index for the web cam

# Loop to input data
while True:
    try:
        # Update currentDataPoint
        
        ###currentDataPoint[0], currentDataPoint[1] = currentDataPoint[0].decode(encoding='utf-8'), currentDataPoint[1].decode(encoding='utf-8')
        
        #Add DateAndTime to the beginning of the list
                
        # Set image name to be currentDateTime
        ###imageName = currentDateTime + ".jpg"
        
        # Read image from camera
        ###retval, image = cam.read()
        
        # Save the image
        ###cv2.imwrite(imageSavePath + "/" + imageName, image)
        
        # Delay for 0.5 second(s)
        ###time.sleep(0.5)
        
        # Store data into lightAndTempDatabase
        controller.dataEntry()
        
    except KeyboardInterrupt:
        break

###del(cam)
controller.dbCursor.close()
controller.dbConn.close()
sys.exit()
