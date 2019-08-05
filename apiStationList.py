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
import json
# Road station IDs and such can be pulled from the digitraffic API weather sensor metadata.
#https://tie.digitraffic.fi/api/v1/metadata/weather-stations
# Information for a specific sensor can be found from
#https://tie.digitraffic.fi/api/v1/data/weather-data/ID
# The information is in JSON format.

def returnStationList():
  # Create an empty list to append tuples containing the relevant information.
  stationList = []
  # Retrieve the metadata for road weather sensors.
  roadMetaDataResponse = requests.get("https://tie.digitraffic.fi/api/v1/metadata/weather-stations")

  # Check if the GET request is successfull. Return false otherwise.
  if (roadMetaDataResponse.status_code == 200):
    # Parse the JSON data
    parsedMetaData = json.loads(roadMetaDataResponse.text)
    for entry in parsedMetaData["features"]:
      # Append the tuple to the list.
      # Use try/except in order to catch malformed entries to catch bad entries
      try:
        stationList.append((entry["properties"]["names"]["en"],entry["properties"]["municipality"],entry["properties"]["province"],entry["properties"]["roadStationId"]))
      except KeyError:
        stationList.append((entry["properties"]["name"],entry["properties"]["municipality"],entry["properties"]["province"],entry["properties"]["roadStationId"]))

  elif (roadMetaDataResponse.status_code == 404):
    return false


  # Return the list.
  return stationList

print(len(returnStationList()))
