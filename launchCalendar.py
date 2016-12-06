from bs4 import BeautifulSoup as bs4
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

TAG_RE = re.compile(r'<[^>]+>')
AMP_RE = re.compile(r'&amp;')
APO_RE = re.compile(r'&#039;')

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
  """
    Shows basic usage of the Google Calendar API.

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

def writeEvent(fields):
  # Refer to the Python quickstart on how to setup the environment:
  # https://developers.google.com/google-apps/calendar/quickstart/python
  # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
  # stored credentials.
  titleText = fields[0]
  locationText = fields[1]
  descriptionText = fields[2]
  startTime = fields[3]
  endTime = fields[4]
  launchId = fields[5]
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
  # Increment afternoon time by 12, except for high noon
  if ampm == "PM" and time[0] != "12":
    time[0] = int(time[0]) + 12
  # Change 12 am to 0 o'clock in military time
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

def splitTimeFields(timeString):
  time_time = ""
  time_ampm = ""
  time_utcref = ""
  if("AM" in timeString):
    time_ampm = "AM"
    time_time = timeString.split(" AM")[0]
  elif("PM"in timeString):
    time_ampm = "PM"
    time_time = timeString.split(" PM")[0]
  time_utcref = timeString.split("UTC")[1].strip(")")
  return time_time, time_ampm, time_utcref

def convertLaunchData(fields):
      # Convert the Time to a RFC3336 Standard, required by Google API
      # def formatDateToGoogleAPI(year, date, time, ampm, utcRef):
      launchFields_year = datetime.datetime.now().strftime("%Y")
      stime,etime = formatDateToGoogleAPI(launchFields_year,fields[1],fields[2],fields[3],fields[4])
      titleText = fields[6]+" Satellite Launch via "+fields[7]
      global launchesCount
      launchesCount += 1
      # writeEvent(titleText, locationText, descriptionText, startTime, endTime, launchId):
      return titleText,fields[5],fields[-1],stime,etime,fields[0]

# Used by Beautiful Soup
def launch_table(tag):
  return tag.table and tag.has_attr('class') and tag.has_attr('id')

def getAllLaunches():
  launchEntry = 0
  tableDepth = 0
  launchEvents = list()
  global listCount
  try:
    # Grab the entire page
    launchCalHandle = urllib.request.urlopen('http://www.spaceflightinsider.com/launch-schedule/')
    launchCalHtml = launchCalHandle.read()
    soup = bs4(launchCalHtml, 'html.parser')
    # Cleanup the Launch Entries as a string with consistent spacing, allows
    # better modularization of the script.
    for launchEvent in soup.body.find_all(launch_table)[1:]:
      # Increment the list counter
      listCount += 1
      launchFields = list()
      launchString = re.sub(' +', ' ', launchEvent.prettify().replace('\n', ' ').replace('\r', ''))
      # print(launchString)
      # Get the launchID
      launchFields.append(launchString.split('"launchcalendar" id="')[1].split('"> <tr>')[0].strip())
      # Get the date, bypass non-hard-scheduled launches
      launchFields.append(launchString.split('</span> <span>')[1].split(' </span>')[0].strip())
      if(
      not('Jan' in launchFields[-1]) and not('Feb' in launchFields[-1]) and
      not('Mar' in launchFields[-1]) and not('Apr' in launchFields[-1]) and
      not('May' in launchFields[-1]) and not('Jun' in launchFields[-1]) and
      not('Jul' in launchFields[-1]) and not('Aug' in launchFields[-1]) and
      not('Sep' in launchFields[-1]) and not('Oct' in launchFields[-1]) and
      not('Nov' in launchFields[-1]) and not('Dec' in launchFields[-1])):
        continue
      # Get the time, bypass non-hard-scheduled launches
      if("Time" in launchString):
        if("TBD" in launchString.split('<th> Time </th> <td>')[1].split(' </td>')[0].strip()):
          continue
        else:
          tempTime = splitTimeFields(launchString.split('<th> Time </th> <td>')[1].split(' </td>')[0].strip())
          for timeField in tempTime:
            launchFields.append(timeField)
      else:
        continue
      # Get the Location
      launchFields.append(launchString.split('<th> Location </th> <td>')[1].split('</td>')[0].strip())
      # Get the Satellite and launch vehicle
      launchFields.append(launchString.split('<th colspan="2">')[1].split('</th>')[0].strip())
      if("<wbr>" in launchString.split('<br/>')[1].split('</td>')[0].strip()):
        launchFields.append(re.sub(' </wbr>', '', re.sub(' <wbr> ', '', launchString.split('<br/>')[1].split('</td>')[0].strip())))
      else:
        launchFields.append(launchString.split('<br/>')[1].split('</td>')[0].strip())
      # Get the description
      launchFields.append(launchString.split('"description" colspan="2"> <p>')[1].split('</p>')[0].strip())
      # Convert Stored Data to writeEvent()
      writeEvent(convertLaunchData(launchFields))
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
