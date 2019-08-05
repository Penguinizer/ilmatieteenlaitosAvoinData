# File: apiSTationList.py
# Contains functions:
# * returnStationList()
# Purpose of function:
# To pull up an up to date list of weather stations and road weather stations so that the user may select the relevant ones. 
# Inputs: none
# Outputs: List of Weather Stations containing:
#  * Station name in English
#  * Station municipality
#  * Station province
#  * Station ID

import requests
import xml.etree.cElementTree as ET
# Road station IDs and such can be pulled from the digitraffic API weather sensor metadata.
#https://tie.digitraffic.fi/api/v1/metadata/weather-stations
# Information for a specific sensor can be found from
#https://tie.digitraffic.fi/api/v1/data/weather-data/ID
# The information is in JSON format.

def returnStationList():
  # Create an empty list to append tuples containing the relevant information.
  stationList = []
  # Retrieve current road weather sensor data from the FMI API.
  apiDataResponse = requests.get("http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=livi::observations::road::finland::multipointcoverage")

  # Check if the GET request is successfull. Return false otherwise.
  if (apiDataResponse.status_code == 200):
    # Parse the XML into something usable.
    dataTree= ET.fromstring(apiDataResponse.text)
    for child in dataTree[0][0][4][0][0][0]:
      stationList.append((child[0][1].text,child[0][5].text,child[0][0].text))
  elif (apiDataResponse.status_code == 404):
    return false


  # Return the list.
  return stationList
tmp = returnStationList()
print(tmp[0])
print (len(tmp))
