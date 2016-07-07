#!python

""" 
This class file will be used to create objects
for each serial port being read from.

"""

import time
import serial
import sqlite3

class DataDevice(object):
    """A class that makes devices from serial ports
       
       device: String of path to device file
       location: String of physical device location
       dataFields: Dictionary of sensors on device as key
                   and data SQL data type as value
       databasePath: String of path to database
       
    """
    def __init__(self, device, name, location, dataFields, databasePath):
        self.device = device
        self.deviceName = name
        self.location = location
        self.dataFields = dataFields
        self.dataTable = name + "_" + location + "Table"
        self.dbPath = databasePath
        
        self.port = self.serialPort()
        self.createDataTable()
        
    
    def description(self):
        """Print out the DataDevice features
        """
        print(self.device)
        print(self.deviceName)
        print(self.location)
        print(self.dataFields)
    
    def serialPort(self):
        """Define which port the device is connected to,
           the baud rate, and time between signals.
        """
        ser = serial.Serial(self.device, 9600, timeout=500)
        return ser
    
    def createDataTable(self):
        """Create a data table in the database if it does not exist yet.
        """
        self.dataTableHeaders = self.createTableHeaders()
        self.dbConn = sqlite3.connect(self.dbPath)
        self.dbCursor = self.dbConn.cursor()
        self.dbCursor.execute('CREATE TABLE IF NOT EXISTS ' + self.dataTable + "(" + self.dataTableHeaders + ");")
        
        print("Data table is created.")
    
    def createTableHeaders(self):
        """Create data table headers for table in database
        """
        counter = 0
        self.dataTableHeaders = ''
        for key, value in self.dataFields.items():
            if counter < (len(self.dataFields)-1):
                self.dataTableHeaders += key + ' ' + value + ', '
                counter += 1
            else:
                self.dataTableHeaders += key + ' ' + value
        
        return self.dataTableHeaders
    
    def dataEntry(self):
        """This function is to check length of dataList against number of columns in table.
           After confirming correct length of dataList, enter new row into dataTable or
           ask for the correct number of attributes in the entry.
        """
        
        dataList = self.dataRead()
        executionString = "INSERT INTO " + self.dataTable + " VALUES("
        if len(dataList) == len(self.dataFields):
            for i, item in enumerate(dataList[:-1]):
                item = dataList[i]
                executionString += dataList[i] + ', '
            executionString += dataList[-1] + ");"
            print("Inserting into table {}".format( executionString ))
            try:
                self.dbCursor.execute(executionString)
                self.dbConn.commit()
            except sqlite3.Error as e:
                print ("ERROR: ", e.message)
            
        else:
            print("The number of data attributes being entered does not match the number of columns in the table.")
    
    def dataRead(self):
        """Read the data from serial port.
        """
        currentDataPoint = self.port.readline().split()
        for i, item in enumerate(currentDataPoint):
            item = currentDataPoint[i].decode(encoding='utf-8')
            currentDataPoint[i] = item

        currentDataPoint.reverse()
        currentDataPoint.append(time.strftime("%Y%m%d-%H%M%S"))
        currentDataPoint.reverse()
        
        print(currentDataPoint)
        return currentDataPoint
