# mileGO - A simple mile tracker

## What is it?
Designed to be used as a webapp to allow users to track multiple vehicles' miles. The user, once a vehicle has been selected, can do one of the following tasks:

- **Current Month  Report**: simple, reports whether the current vehicle is on track with monthly miles
- **Compare Month Miles**: straightforward - compare one month to another in terms of miles spent
- **Weekly Data Entry**: enter the odometer reading for the (past) week
- **Update Year Limit**: adjust the current vehicle's maximum amount of miles for a year

More features could be added as the project grows, but the project's essence lies in the features above.

## How is a vehicle represented?
With simplicity in mind, vehicle data is stored in JSON format. As of right now, each vehicle needs to have its own `.json` file. That file contains the following members:

- **Name**: the name of the vehicle
- **yearLimit**: the maximum amount of miles to spend on a year
- **yearBudget**: the remaining miles to use for the remaining months
- **monthBudget**: the miles to spend (or ones spent) for every month
- **miles**: each month's odometer readings

## API functionality
Below is a summary of `api.py`, the API that supplies the functionality for the app.

### *Global variables*
- **currentVehiclePath**: string that holds the path to the current vehicle
- **vehicleData**: stores a JSON object with the current vehicle info

### *Functions*
- **readVehicleData()**
  - **Input(s)**: none
  - **Output(s)**: none
  - **Side Effect(s)**: populates `vehicleData` with current vehicle's data
  - **Note(s)**: none

- **setCurrentVehicle(vehiclePath)**
  - **Input(s)**: vehiclePath - string of desired vehicle's filepath
  - **Output(s)**: none
  - **Side Effect(s)**: sets `currentVehiclePath` to desired vehicle's filepath
  - **Note(s)**: should be called before reading/writing data

- **writeVehicleData()**
  - **Input(s)**: none
  - **Output(s)**: none
  - **Side Effect(s)**: writes `vehicleData` into current vehicle's file
  - **Note(s)**: should be used with any sort of operation that changes the state of `vehicleData`

- **setYearLimit(newLimit)**
  - **Input(s)**: newLimit - integer with new desired yearly limit
  - **Output(s)**: none
  - **Side Effect(s)**: populates `yearLimit` of current vehicle with `newLimit` 
  - **Note(s)**: assumes the limit is valid (i.e not negative)

- **getMonthMiles(targetMonth)**
  - **Input(s)**: targetMonth [0 - 11] - the (only) month to get the miles of
  - **Output(s)**: `-1` if failure, or `targetMonth`'s miles
  - **Side Effect(s)**: 
  - **Note(s)**: Unless `targetMonth` == first of the year, use previous month's last entry as reference. Depends on `setOdometerValue(targetMonth, targetWeek, value)` for correct functionality (See function code).

- **setOdometerValue(targetMonth, targetWeek, value)**
  - **Input(s)**: targetMonth [0 - 11], targetWeek [0 - 3], value - self explanatory
  - **Output(s)**: -1 if failure, 0 if success
  - **Side Effect(s)**: adjusts `yearBudget` from (calculated) miles entered 
  - **Note(s)**: If valid, updates `miles` with a new entry on `targetMonth` and `targetWeek`. If there's unset entries before current one, it will update those as well with the current value.

- **getPreviousEntry(targetMonth, targetWeek)**
  - **Input(s)**: targetMonth [0 - 11], targetWeek [0 - 3]
  - **Output(s)**: the corresponding odometer value for the entry before `targetMonth`,`targetWeek` entry.
  - **Side Effect(s)**: none 
  - **Note(s)**: Internal - shouldn't be used

- **getNextEntry(targetMonth, targetWeek)**
  - **Input(s)**: targetMonth [0 - 11], targetWeek [0 - 3]
  - **Output(s)**: the corresponding odometer value for the entry after `targetMonth`,`targetWeek` entry.
  - **Side Effect(s)**: none 
  - **Note(s)**: Internal - shouldn't be used

- **getEntryTargets(targetMonth, targetWeek)**
  - **Input(s)**: targetMonth [0 - 11], targetWeek [0 - 3]
  - **Output(s)**: the corresponding "gaps"/unwritten values before a `targetMonth`,`targetWeek` entry.
  - **Side Effect(s)**: none 
  - **Note(s)**: Internal - shouldn't be used