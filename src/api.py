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

""" # @state: testing
def setOdometerValue(targetMonth, targetWeek, value):
    # Enforces no gaps between entries (if there is gap, fill it with current value)
    # AND enforces entries are in increasing order
    
    if value < 0:
        print('ERR: value is negative')
        return -1

    prevValue = -1
    targets = []

    # First week of a non-first month uses last week of previous one as reference
    if targetWeek == 0 and targetMonth != 0:
        prevValue = vehicleData["miles"][targetMonth-1]["week"][3]
    # A non-first week uses the week before as reference
    if targetWeek != 0:
        # Keep track of any "gaps" (targets) to cover
        for i in range(0, targetWeek, 1):
            d = vehicleData["miles"][targetMonth]["week"][i]
            if d == -1:
                targets.append(i)
            else:
                prevValue = d
    
    print('DBG: prevValue', prevValue, 'targets', targets)
    # Validate value
    if targetMonth == 0 and targetWeek == 0:
        if value < vehicleData["miles"][0]["week"][1]:
            return -1
        else:
            vehicleData["miles"][targetMonth]["week"][0] = value
    elif value < prevValue:
        return -1
    else:
        # Update all necessary targets
        vehicleData["miles"][targetMonth]["week"][targetWeek] = value
        for i in targets:
            vehicleData["miles"][targetMonth]["week"][i] = value
            

    #Update yearly budget (needs getCurrentMilesUptoMonth)
    #vehicleData["yearBudget"] = 

    writeVehicleData()
    return 0 """