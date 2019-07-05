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

# @status: working (needs set testing)
def getMonthMiles(targetMonth):
    # Assumes the first week of a current/past month can never be unset
    # AND assumes entries are in increasing order

    # Shouldn't be able to get a future's month miles 
    monthData = vehicleData["miles"][targetMonth]["week"]
    if monthData[0] == -1:
        return -1
    
    monthData = [w for w in monthData if w >= 0]

    # Any month other than first has a previous month starting point
    if targetMonth != 0:
        return max(monthData) - vehicleData["miles"][targetMonth-1]["week"][3]
    
    return max(monthData) - monthData[0]

# @state: testing
def setOdometerValue(targetMonth, targetWeek, value):

    if value < 0:
        return -1
    
    p = getPreviousEntry(targetMonth, targetWeek)
    n = getNextEntry(targetMonth, targetWeek)

    if value < p or (value > n and n != -1):
        return -1

    # Be sure to cover gaps
    targets = (targetMonth, targetWeek)
    if p == -1:
        targets = getEntryTargets(targetMonth, targetWeek)

    print(targets)

    # Update month budget
    # Update year budget
    # Modify targets to hold value
    # Write vehicle data
    # return 0
    
# @state: working
# @internal
def getEntryTargets(targetMonth, targetWeek):
    # Should have tuples of valid month, week to "cover" in setOdometerValue()
    res = []

    while(vehicleData["miles"][targetMonth]["week"][targetWeek] == -1):
        # Add this specific gap
        res.append((targetMonth, targetWeek))

        # Adjust "going down" the data
        if targetWeek == 0:
            if targetMonth != 0:
                targetMonth -= 1
                targetWeek = 3
            else:
                break
        else:
            targetWeek -= 1

    return res 

# @state: working
# @internal
def getPreviousEntry(targetMonth, targetWeek):
    res = 0
    
    if targetWeek == 0:
        if targetMonth != 0:
            res = vehicleData["miles"][targetMonth-1]["week"][3]
    else:
        res = vehicleData["miles"][targetMonth]["week"][targetWeek-1]
    
    return res

# @state: working
# @internal
def getNextEntry(targetMonth, targetWeek):
    res = 0

    if targetWeek == 3:
        if targetMonth != 11:
            res = vehicleData["miles"][targetMonth+1]["week"][0]
    else:
        res = vehicleData["miles"][targetMonth]["week"][targetWeek+1]
    
    return res