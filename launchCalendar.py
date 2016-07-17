import urllib.request
import urllib.error
import re
import datetime
import calendar

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

launchesCount = 0
listCount = 0
totalDeleted = 0

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
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'LaunchScript'
LAUNCHCALENDARID = 'cnogq69s3e5p64ph1mmfusk64c@group.calendar.google.com'

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
  credential_path = os.path.join(credential_dir, 'launch-script.json')
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

def clearCalendar():
  """
    Get OAuth2 Credentials to Write to the Calendar.
  """
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http)
  global totalDeleted
  """
    Insert the new Event in the Launch Calendar
  """
  # First parse through the entire calendar and pull out each event, grabbing
  # the unique event ID field, then use that field to request an event delete
  # from the API.
  events = service.events().list(
    calendarId=LAUNCHCALENDARID,
    maxResults=1000,
    singleEvents=True,
    orderBy='startTime'
    ).execute()
  # for event in events["items"]:
    # print("Event in list, ID %s"%(event["id"]))
    # print("  %s"%(event["summary"]))
    # print("  %s"%(event["start"]['dateTime']))
  for event in events["items"]:
    print("Deleting event ID %s"%(event["id"]))
    print("  %s"%(event["summary"]))
    print("  %s"%(event["start"]['dateTime']))
    service.events().delete(calendarId=LAUNCHCALENDARID, eventId=event["id"]).execute()
    totalDeleted += 1

def readAllEvents():
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

def writeEvent(titleText, locationText, descriptionText, startTime, endTime, launchId):
  # Refer to the Python quickstart on how to setup the environment:
  # https://developers.google.com/google-apps/calendar/quickstart/python
  # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
  # stored credentials.
  print(titleText)
  print(startTime)
  event = {
    'summary': titleText,
    'location': locationText,
    'description': descriptionText,
    'start': {
      # Must be of the format: 2016-02-22T15:00:00-07:00
      # where the end date and time is Feb 22, 2016 3PM local time to UTC-7
      # timezone.
      'dateTime': startTime,
    },
    'end': {
      # Must be of the format: 2016-02-22T15:00:00-07:00
      # where the end date and time is Feb 22, 2016 3PM local time to UTC-7
      # timezone.
      'dateTime': endTime,
    },
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'popup', 'minutes': 15},
        {'method': 'popup', 'minutes': 60},
      ],
    },
  }
  """
    Get OAuth2 Credentials to Write to the Calendar.
  """
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('calendar', 'v3', http=http)
  """
    Insert the new Event in the Launch Calendar
  """
  try:
    event = service.events().insert(
      calendarId=LAUNCHCALENDARID,
      body=event
    ).execute()
    print('Event created: %s'%(event.get('htmlLink')))
  except:
    print("There was an error writing launch event %s to the Google Calendar"%(launchId))
    print(event)

TAG_RE = re.compile(r'<[^>]+>')
AMP_RE = re.compile(r'&amp;')
APO_RE = re.compile(r'&#039;')
def remove_tags(text):
  """
    Remove any HTML Tags from a string
    This also includes reformatting HTML special character escapes to regular 
    text.
  """
  text = AMP_RE.sub('&', text)
  text = APO_RE.sub('\'', text)
  return TAG_RE.sub('', text)

def formatDateToGoogleAPI(year, date, time, ampm, utcRef):
  """
    Compliance with RFC3339
    Needs to be formatted as: 
    2015-05-28T09:00:00-07:00
  """
  # Convert Date to the correct format
  date = date.split()
  date[0] = {v: k for k,v in enumerate(calendar.month_abbr)}[date[0]]
  sdate = "%s-%02d-%02d"%(year,int(date[0]),int(date[1]))
  # Convert 12 hour Time to 24 hour
  time = time.split(':')
  if ampm == "PM":
    time[0] = int(time[0]) + 12
  elif ampm == "AM" and time[0] == "12":
    time[0] = int(time[0]) - 12
  stime = "%02d:%02d:00"%(int(time[0]),int(time[1]))
  etime = ''
  edate = ''
  if int(time[0])+1 == 24:
    etime = "%02d:%02d:00"%(0,int(time[1]))
    edate = "%s-%02d-%02d"%(year,int(date[0]),int(date[1])+1)
  else:
    etime = "%02d:%02d:00"%(int(time[0])+1,int(time[1]))
    edate = "%s-%02d-%02d"%(year,int(date[0]),int(date[1]))
  # Convert UTC Reference to RFC3339 format: -7 becomes -07:00
  if utcRef.find("-") > -1:
    utcRef = utcRef.strip('-')
    sign = "-"
  else:
    sign = "+"
  if utcRef.find(".") > -1:
    utcRefHr = int(float(utcRef))
    utcRefMin = int(float(utcRef)*60)%60
    utcRef = "%02d:%02d"%(utcRefHr,utcRefMin)
  else:
    utcRef = "%02d:00"%(int(float(utcRef)))
  utcRef = sign+utcRef
# Now put it all together
  sdateTimeRfc3339 = sdate+"T"+stime+utcRef
  edateTimeRfc3339 = edate+"T"+etime+utcRef
  return sdateTimeRfc3339, edateTimeRfc3339

def parseLaunchFields(launchFields,launchId):
  """
    The purpose of this function is to take as input a single HTML Table
    row which is seen in the Space Flight Insider's Launch Calendar website,
    parse and format fields needed for writing to the Google Calendar API.

    This function assumes all needed fields are present thus non-scheduled
    launches are parsed out.
  """
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
    descriptionElement = 0
    for element in launchFields:
      descriptionElement += 1
      if element.find("class=\"description\">") > -1:
        break
    launchesCount += 1
    # Launch Vehicle
    launchVehicle = remove_tags(launchFields[6].strip())
    # Launch Payload
    launchPayload = remove_tags(launchFields[2].strip())
    # Launch Date/Time Convert to RFC3339 Format
    launchTime = remove_tags(launchFields[14].strip())
    rawTime,amPm,timeZone,utcRef = launchTime.split()
    utcRef = utcRef.strip("(UTC")
    utcRef = utcRef.strip(")")
    launchDate = remove_tags(launchFields[1].strip().strip("NET"))
    year = '2016'
    date,edate = formatDateToGoogleAPI(year, launchDate, rawTime, amPm, utcRef)
    # Launch Location
    launchLocation = remove_tags(launchFields[11].strip())
    # Launch Description
    launchDescription = remove_tags(launchFields[descriptionElement].strip())
    # Launch Payload Manufacturer Logo
    if("img src" in launchFields[4]):
      *blah,launchPayloadLogoURL = launchFields[4].strip().split("http")
      launchPayloadLogoURL,*blah = launchPayloadLogoURL.split(".png")
      launchPayloadLogoURL = "http"+launchPayloadLogoURL+".png"
    # Launch Vehicle Manufacturer Logo
    if("img src" in launchFields[5]):
      *blah,launchVehicleLogoURL = launchFields[5].strip().split("http")
      launchVehicleLogoURL,*blah = launchVehicleLogoURL.split(".png")
      launchVehicleLogoURL = "http"+launchVehicleLogoURL+".png"
    writeEvent(
      launchVehicle+" Launch, Payload: "+launchPayload,
      launchLocation,
      launchDescription,
      date,
      edate,
      launchId
    )

def getAllLaunches():
  launchEntry = 0
  tableDepth = 0
  launchFields = list()
  launchId = ""
  try:
    with urllib.request.urlopen('http://www.spaceflightinsider.com/launch-schedule/') as urlfh:
      for line in urlfh:
        line = line.decode('utf-8')
        # Find start of a launch schedule entry
        if ("<table class=" in line) and ("launchcalendar" in line):
          launchEntry = 1
          *blah,launchId = line.split("id=\"")
          launchId,*blah = launchId.split("\">")
          launchId = launchId.strip("-")
          print(launchId)
          continue
        # Capture when at the end of a launch entry
        elif (launchEntry is 1) and ("</table" in line) and (tableDepth is 0):
          launchEntry = 0
          parseLaunchFields(launchFields,launchId)
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
  # readAllEvents
  clearCalendar()
  getAllLaunches()
  print("Total launches listed: %d"%(listCount))
  print("Total scheduled launches: %d"%(launchesCount))
  print("Total events deleted: %s"%(totalDeleted))
