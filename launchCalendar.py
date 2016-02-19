import urllib.request
import urllib.error
import re

launchesCount = 0
listCount = 0

"""
  Remove any HTML Tags from a string
"""
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def parseLaunchFields(launchFields):
  global launchesCount
  global listCount
  listCount += 1
  # If the launch has no determined date yet, skip it
  if "TBD" in launchFields[1]:
    return
  # If the launch has no determined time yet, skip it
  elif "TBD" in launchFields[14]:
    return
  else:
    print("---------------------------------")
    print("New Launch Fields")
    print("---------------------------------")
    # print("Raw:")
    # print(launchFields)
    # print("")
    launchesCount += 1
    # Launch Vehicle
    launchVehicle = remove_tags(launchFields[6].strip())
    print(launchVehicle)
    # Launch Payload
    launchPayload = remove_tags(launchFields[2].strip())
    print(launchPayload)
    # Launch Time
    launchTime = remove_tags(launchFields[14].strip())
    print(launchTime)
    # Launch Date
    launchDate = remove_tags(launchFields[1].strip().strip("NET"))
    print(launchDate)
    # Launch Location
    launchLocation = remove_tags(launchFields[11].strip())
    print(launchLocation)
    # Launch Description
    launchDescription = remove_tags(launchFields[20].strip())
    print(launchDescription)
    # Launch Payload Manufacturer Logo
    if("img src" in launchFields[4]):
      *blah,launchPayloadLogoURL = launchFields[4].strip().split("http")
      launchPayloadLogoURL,*blah = launchPayloadLogoURL.split(".png")
      launchPayloadLogoURL = "http"+launchPayloadLogoURL+".png"
      print(launchPayloadLogoURL)
    # Launch Vehicle Manufacturer Logo
    if("img src" in launchFields[5]):
      *blah,launchVehicleLogoURL = launchFields[5].strip().split("http")
      launchVehicleLogoURL,*blah = launchVehicleLogoURL.split(".png")
      launchVehicleLogoURL = "http"+launchVehicleLogoURL+".png"
      print(launchVehicleLogoURL)
    print("")

def getAllLaunches():
  launchEntry = 0
  tableDepth = 0
  launchFields = list()
  try:
    with urllib.request.urlopen('http://www.spaceflightinsider.com/launch-schedule/') as urlfh:
      for line in urlfh:
        line = line.decode('utf-8')
        # Find start of a launch schedule entry
        if ("<table class=" in line) and ("launchcalendar" in line):
          launchEntry = 1
          continue
        # Capture when at the end of a launch entry
        elif (launchEntry is 1) and ("</table" in line) and (tableDepth is 0):
          launchEntry = 0
          parseLaunchFields(launchFields)
          launchFields = []
          continue
          # break
        # Keep Track of Depth of Tables When parsing Launch Fields
        if (launchEntry is 1) and ("<table" in line):
          tableDepth += 1
          continue
        elif (launchEntry is 1) and ("</table" in line):
          tableDepth -= 1
          continue

        # Store Launch Entry
        if(launchEntry is 1):
          launchFields.append(line)
  except urllib.error.HTTPError:
    print("There was an error accessing the Space Flight Insider Launch Schedule.")
    print("The server could be down or having issues. Try again.")
  except urllib.error.URLError:
    print("There was an error decoding the URL for the Space Flight Insider Launch Schedule. :::nodename not known :::")
    print("Check that your computer has access to the Internet.")

getAllLaunches()
print("Total scheduled launches: %d"%(launchesCount))
print("Total launches listed: %d"%(listCount))
