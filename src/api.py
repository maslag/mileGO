import json
from datetime import date, timedelta

currentVehiclePath = '' # Path to JSON to current vehicle
vehicleData = 0 # Vehicle data for current vehicle

# @status: working
def readVehicleData():
    global vehicleData
    targetFile = open(currentVehiclePath, 'r')
    vehicleData = json.load(targetFile)
    targetFile.close()

# @status: working
def setCurrentVehicle(vehiclePath):
    global currentVehiclePath
    currentVehiclePath = vehiclePath

# @status: working
def writeVehicleData():
    global vehicleData
    targetFile = open(currentVehiclePath, 'w')
    json.dump(vehicleData, targetFile)
    targetFile.close()

# @status: working
def setYearLimit(newLimit):
    vehicleData["yearLimit"] = newLimit
    writeVehicleData()