# File: apiRequest.py
# Contains functions:
# sendAPIRequest(stationTuple, startDateString, endDateString)
# Purpose of function:
# To send an api request to the FMI open api in order to retrieve saved weather data. The data is fetched with a HTTP GET request and sent in XML format to another function responsible for parsing it.
# Inputs:
# * A tuple containing the name of the weather station, its type and its SID.
# * A pair of strings containing dates between which saved data is to be fetched.
# Outputs:
# * List containing XML entries containing the data and metadata from the API.

import requests
import datetime
def sendAPIRequest(stationTuple, startDateString, endDateString):
  # Create an empty list to put data into.
  apiResponseList = []
  # Convert startDate and endDate strings into date objects.
  startDateObj = datetime.datetime.strptime(startDateString, '%Y-%m-%d').date()
  endDateObj = datetime.datetime.strptime(endDateString, '%Y-%m-%d').date()
  # The API allows for a maximum of 30 days of data to be pulled at one time.
  # Calculate the difference in days between the given dates in order to ensure
  # requests fit within specified amount of time.
  timeDifference = abs(endDateObj-startDateObj)
  print (timeDifference)
  print (startDateObj+timeDifference)
  if (timeDifference.days > 30):
    # Iterate through requested time in 30 day chunks.
    print("dong")
  else:
    # Generating a string for the API request.
    requestString = ("http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::hourly::timevaluepair&fmisid="+str(stationTuple[2])+"&starttime="+str(startDateObj)+"&endtime="+str(endDateObj)+"&")
    # Sending request to API.
    apiResponseList.append(requests.get(requestString))
  return apiResponseList
  # return "dong"
def apiTest():
    return sendAPIRequest(('Kuopio Maaninja', 'Kuopio', '101572', 'weather'),"2013-02-26", "2013-03-26")

print(apiTest())
