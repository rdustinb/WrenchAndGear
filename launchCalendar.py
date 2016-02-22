import urllib.request
import urllib.error
import re
import datetime

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

launchesCount = 0
listCount = 0

"""
  Google API Stuff
"""
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'LaunchScript'
LAUNCHCALENDARID = '8prjuab6hlhna6fq79blg5697c@group.calendar.google.com'

"""
  The following functions are used to install credentials from a file called
  'client_secret.json' and place them in a usual install directory. The 'main'
  function then uses OAuth2 to simply check the next 10 events from whichever 
  calendarId the user specifies through LAUNCHCALENDARID of the logged in user
  who first ran the get_credentials() function.
"""
def get_credentials():
  """Gets valid user credentials from storage.

  If nothing has been stored, or if the stored credentials are invalid,
  the OAuth2 flow is completed to obtain the new credentials.

  Returns:
      Credentials, the obtained credential.
  """
  home_dir = os.path.expanduser('~')
  credential_dir = os.path.join(home_dir, '.credentials')
  if not os.path.exists(credential_dir):
    os.makedirs(credential_dir)
  credential_path = os.path.join(credential_dir,
                                 'launch-script.json')

  store = oauth2client.file.Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
      credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
      credentials = tools.run(flow, store)
    print('Storing credentials to ' + credential_path)
  return credentials

def testReadEvents():
  """Shows basic usage of the Google Calendar API.

  Creates a Google Calendar API service object and outputs a list of the next
  10 events on the user's calendar.
  """
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http)

  now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
  print('Getting the upcoming 10 events')
  eventsResult = service.events().list(
    calendarId=LAUNCHCALENDARID, timeMin=now, maxResults=10, singleEvents=True,
    orderBy='startTime').execute()
  events = eventsResult.get('items', [])

  if not events:
    print('No upcoming events found.')
  for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
"""
  ------------
"""

def writeEvent(titleText, locationText, descriptionText, startTime, endTime):
  # Refer to the Python quickstart on how to setup the environment:
  # https://developers.google.com/google-apps/calendar/quickstart/python
  # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
  # stored credentials.
  event = {
    'summary': titleText,
    'location': locationText,
    'description': descriptionText,
    'start': {
      'dateTime': endTime,
    },
    'end': {
      'dateTime': endTime,
    },
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'popup', 'minutes': 15},
      ],
    },
  }

  event = service.events().insert(
    calendarId=LAUNCHCALENDARID,
    body=event
  ).execute()
  print('Event created: %s'%(event.get('htmlLink')))

"""
  Remove any HTML Tags from a string
"""
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def convertTime(hour,minute,utcRef):
  newHour = ((int(hour) - int(float(utcRef))) + 24)%24
  if(int(minute) < int((float(utcRef)*60)%60)):
    newHour = ((newHour - 1)+24)%24
    newMinute = (int(minute) - int(float(utcRef)*60))%60
  else:
    newHour = newHour
    newMinute = (int(minute) - int(float(utcRef)*60))%60
  return (newHour,newMinute)

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
    """
      Need to Convert the time to UTC for ease of maintenance.
    """
    rawTime,amPm,timeZone,utcRef = launchTime.split()
    utcRef = utcRef.strip("(UTC")
    utcRef = utcRef.strip(")")
    if(rawTime.count(":") == 2):
      hour,minute,sec = rawTime.split(":")
    elif(rawTime.count(":") == 1):
      hour,minute = rawTime.split(":")
    print("%s Time: %s %s"%(timeZone,rawTime,utcRef))
    hour,minute = convertTime(hour,minute,utcRef)
    print("UTC Time: %d:%02d"%(hour,minute))
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

if __name__ == '__main__':
  # Install the credentials from the client_secret.json file located in this
  # same directory. If you don't have permission to write to this calendar, you
  # won't have this .json file.
  get_credentials()
  # testReadEvents()
  getAllLaunches()
  print("Total scheduled launches: %d"%(launchesCount))
  print("Total launches listed: %d"%(listCount))
