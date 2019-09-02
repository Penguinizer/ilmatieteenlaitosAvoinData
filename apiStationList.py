# File: apiSTationList.py
# Contains functions:
# * returnStationList()
# Purpose of function:
# To pull up an up to date list of weather stations and road weather stations so that the user may select the relevant ones. 
# Inputs: none
# Outputs: List of Weather Stations containing:
#  * Station name
#  * Station municipality
#  * Station ID

import requests
import xml.etree.cElementTree as ET
from time import sleep
# Road station IDs and such can be pulled from the digitraffic API weather sensor metadata.
#https://tie.digitraffic.fi/api/v1/metadata/weather-stations
# Information for a specific sensor can be found from
#https://tie.digitraffic.fi/api/v1/data/weather-data/ID
# The information is in JSON format.

def returnRoadStationList():
  # Create an empty list to append tuples containing the relevant information.
  stationList = []
  # Retrieve current road weather sensor data from the FMI API.
  apiRoadResponse = requests.get("http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=livi::observations::road::finland::multipointcoverage")
  # print("Road API: "+str(apiRoadResponse))
  # Check if the GET request is successfull. Return false otherwise.
  if (apiRoadResponse.status_code == 200):
    # Parse the XML into something usable.
    roadDataTree = ET.fromstring(apiRoadResponse.text)
    # Iterate through the road weather stations.
    for child in roadDataTree[0][0][4][0][0][0]:
      # Retrieve the name, municipality and FMISID of the road weather staiton.
      try:
        stationList.append((child[0][1].text,child[0][5].text,child[0][0].text, "road")) 
      except:
        print("Incorrectly formatted data")
  else:
    print("Request 404")
    return false
  # Sort list and return
  stationList.sort(key=lambda tup: tup[0])
  return stationList

def returnWeatherStationList():
  stationList = []
  # Request a list of monitoring stations available on the FMI API.
  apiWeatherResponse = requests.get("http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::ef::stations&networkid=121")
  # print("Weather API: " + str(apiWeatherResponse))
  # Check if the GET response is sucecssfull, return false otherwise.
  if (apiWeatherResponse.status_code == 200):
    # Parse the XML into something usable.
    stationDataTree = ET.fromstring(apiWeatherResponse.text)
    # Iterate through the monitoring stations.
    for child in stationDataTree:
      # Retrieve and save the name, region, FMISID and type.
      try:
        stationList.append((child[0][1].text,child[0][4].text,child[0][0].text,"weather"))
      except:
        print("Incorrectly formatted data")
  else:
    print("Request 404")
    return false

  # Return the list after alphabetical sorting.
  stationList.sort(key=lambda tup: tup[0])
  return stationList

def fetchTest():
  tmp = returnWeatherStationList()
  for n in tmp:
    print(str(n)+'\n')
  print (len(tmp))
  tmp2 = returnRoadStationList()
  for n in tmp2:
    print(str(n)+'\n')
  print(len(tmp2))

fetchTest()
