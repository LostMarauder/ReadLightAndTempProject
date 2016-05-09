"""This file reads data sent to serial port and writes the data to a text file
    continuously.
"""

import os.path  # Import path method to direct to data file

import sys  # Import sys module

import time  # Import sleep method for delay

import serial  # Import module to read serial port

import cv2 # Import cv2 for image capture

# Declare object for controller port, with baud rate 9600, and timeout of 9600
ser = serial.Serial("COM3", 9600, timeout=500)

# Declare path to data file directory
savePath = "C:/Users/Sameer/Desktop/read_light_and_temp/TestData/" + time.strftime("%Y%m%d-%H%M%S")

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
dataFilePath = os.path.join(savePath, saveFile + ".txt")
imageFilePath = os.path.join(savePath, imageSavePath)

# Declare object for file to read and write to
with open(dataFilePath, mode='w', buffering=0) as dataRecord:
    # Print header row to data file
    dataRecord.write("Date-Time" + "\t" + "Light" + "\t" +
                     "Temp C" + "\t" + "Temp F" + "\n")

    cam = cv2.VideoCapture(1)  # Initialize web cam. 1 is the index for the web cam

    # Loop to input data
    while True:

        try:

            currentDateTime = time.strftime("%Y%m%d-%H%M%S")  # Update currentDate

            rate = ser.readline()   # Update value for light reading
            temperatureC = ser.readline()   # Update value for temperature reading
            imageName = currentDateTime + ".jpg" # Set image name to be currentDateTime

            # Print current date, time, and data from serial port
            dataRecord.write(currentDateTime + "\t"
                             + ser.readline())

            # Placed cam variable declaration here before moving

            retval, image = cam.read()  # Read image from camera
            cv2.imwrite(imageSavePath + "/" + imageName, image)     #Save the image


            time.sleep(0.5)  # Delay for 0.5 second(s)
            print(currentDateTime + "\t" + temperatureC)

        except KeyboardInterrupt:
            break

    del(cam)
    sys.exit()
