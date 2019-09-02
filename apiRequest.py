# File: apiRequest.py
# Contains functions:
# sendAPIRequest(stationTuple, startDateString, endDateString, timeStep)
# Purpose of function:
# To send an api request to the FMI open api in order to retrieve saved weather data. The data is fetched with a HTTP GET request and sent in XML format to another function responsible for parsing it.
# Inputs:
# * A tuple containing the name of the weather station, its type and its SID.
# * A pair of strings containing dates between which saved data is to be fetched
# * An integer for the time between datapoints in minutes.
# Outputs:
# * List containing XML entries containing the data and metadata from the API.

import requests
import datetime
def sendAPIRequest(stationTuple, startDateString, endDateString, timeStep):
  # Create an empty list to put data into.
  apiResponseList = []
  # Convert startDate and endDate strings into date objects.
  startDateObj = datetime.datetime.strptime(startDateString, '%Y-%m-%d').date()
  endDateObj = datetime.datetime.strptime(endDateString, '%Y-%m-%d').date()
  # The API allows for a maximum of 30 days of data to be pulled at one time.
  # Calculate the difference in days between the given dates in order to ensure
  # requests fit within specified amount of time.
  timeDifference = abs(endDateObj-startDateObj)
#  print (timeDifference)
#  print (startDateObj+timeDifference)
  # Set a variable for amount of days in a chunk.
  # Hardcoded to 7 as per limitations of query used.
#  print (timeStep)
  daysPerChunk = 7
#  print(daysPerChunk)
  if (timeDifference.days > daysPerChunk):
    # Calculate the amount of 30 day chunks and remaining days over.
    chunkCount, remainder = divmod(timeDifference.days, daysPerChunk)
    dayChunk = datetime.timedelta(days=daysPerChunk)
#    print(str(chunkCount)+ " and " + str(remainder))
    if (stationTuple [3] == 'weather'):
#      print ("Multiple weather station requests")
      # Iterate through the time period entered in 30 day chunks.
      # Sending multiple API requests in order to circumvent 30 day limit.
      for n in range(chunkCount):
        tempStart = startDateObj+(dayChunk*n)
        tempEnd = startDateObj+(dayChunk*(n+1))
#        print (str(tempStart) + " and " + str(tempEnd))
        requestString = ("http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&fmisid="+str(stationTuple[2])+"&starttime="+str(tempStart)+"&endtime="+str(tempEnd)+"&timestep=" + str(timeStep) + "&")
#        print(requestString)
        apiResponseList.append(requests.get(requestString))
      # Send final request for the remaining days not covered by the previous chunks.
      requestString = ("http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&fmisid="+str(stationTuple[2])+"&starttime="+str(endDateObj-(datetime.timedelta(days=remainder)))+"&endtime="+str(endDateObj)+"&timestep=" + str(timeStep)+ "&")
      apiResponseList.append(requests.get(requestString))
    else:
      print ("Road Station not implemented")
  else:
    if (stationTuple[3] == 'weather'):
      # Generating a string for the API request.i
      requestString = ("http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&fmisid="+str(stationTuple[2])+"&starttime="+str(startDateObj)+"&endtime="+str(endDateObj)+"&timestep=" + str(timeStep) + "&")
#      print(requestString)
      # Sending request to API.
      apiResponseList.append(requests.get(requestString))
    else:
      print("Road Station not implemented")
  return apiResponseList
#  return "dong"
def apiTest():
  return sendAPIRequest(('Kuopio Maaninja', 'Kuopio', '101572', 'weather'),"2013-02-01", "2013-02-22", 10)
#  return sendAPIRequest(('Argablargh', 'Kupio', '101572', 'weather'),"2013-01-01", "2013-06-03", 60) 

print(apiTest())
