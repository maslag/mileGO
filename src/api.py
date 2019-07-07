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

# @state: working
def setOdometerValue(targetMonth, targetWeek, value):

    if value < 0:
        return -1
    
    p = getPreviousEntry(targetMonth, targetWeek)
    n = getNextEntry(targetMonth, targetWeek)

    if value < p or (value > n and n != -1):
        return -1

    # Get (month, week) of targets to "fill in"
    targets = [(targetMonth, targetWeek)]
    if p == -1:
        targets = getEntryTargets(targetMonth, targetWeek)
    
    for item in targets:
        vehicleData["miles"][item[0]]["week"][item[1]] = value

    # You should only update the budgets if an actual "change" happened
    if n == -1:
        ref = getPreviousEntry(targets[len(targets)-1][0], targets[len(targets)-1][1])
        miles = 0 if ref == 0 else value - ref
        updateCurrentBudgets(targetMonth, targetWeek, miles)
    
    writeVehicleData()
    return 0

# @state: working
# @internal
def updateCurrentBudgets(targetMonth, targetWeek, miles):
    vehicleData["monthBudget"][targetMonth]["value"] -= miles
    vehicleData["yearBudget"] -= miles
    
    # If we've gone past the year budget, reallocate it to be the year limit / # months left
    if vehicleData["yearBudget"] < 0:
        vehicleData["yearBudget"] = vehicleData["yearLimit"] / (11 - targetMonth)

    # Compute the new avg for the remaining months, and assign it
    avg = vehicleData["yearBudget"] / (11 - targetMonth)

    for m in range(targetMonth+1, 12):
        vehicleData["monthBudget"][m]["value"] = avg
    

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