import urllib.request
import urllib.error

import os

def grabRawPage(localFileOrHttpRequest):
  if localFileOrHttpRequest is "http":
    try:
      launchCalHtml = urllib.request.urlopen('http://www.spaceflightnow.com/launch-schedule/').read().decode("utf-8")
    except urllib.error.HTTPError:
      print("There was an error accessing the Space Flight Insider Launch Schedule.")
      print("The server could be down or having issues. Try again.")
    except urllib.error.URLError:
      print("There was an error decoding the URL for the Space Flight Insider Launch Schedule. :::nodename not known :::")
      print("Check that your computer has access to the Internet.")
  else:
    try:
      with open('testData/launch-schedule.html', 'r') as file: launchCalHtml = file.read()
    except urllib.error.HTTPError:
      print("There was an error accessing the Space Flight Insider Launch Schedule.")
      print("The server could be down or having issues. Try again.")
  # make everything one giant string with only single spaces separating stuff
  launchCalHtml = " ".join(launchCalHtml.replace('\n', '').split())
  return(launchCalHtml)

def formatDataFromRawPage(launchCalHtml):
  # format such that tags always butt up against each other and have no spaces before or after them
  launchCalHtml = launchCalHtml.replace("> <", "><").replace(" <", "<").replace("> ", ">")
  # strip off the footer
  launchCalHtml = launchCalHtml.split("</div></article></div>")[0]
  # strip off the beginning of the page to the calendar events
  launchCalHtml = " ".join(launchCalHtml.split("<div class=\"datename\">")[1:])
  # find weird ascii characters
  launchCalHtml = launchCalHtml.replace("&#8217;", "'").replace("&amp;", "&")
  # split into individual launch events
  launchCalHtml = launchCalHtml.split("<span class=\"launchdate\">")[1:]
  # format individual launches
  for launch in launchCalHtml:
    # Get the mission name
    launchMission = "%s"%(launch.split("mission\">")[1].split("<")[0])
    # Get the launch window
    launchWindow = "%s, %s"%(launch.split("<")[0], launch.split("</span>")[3].split("<")[0])
    # Get the launch site
    launchSite = "%s"%(launch.split("Launch site:</span>")[1].split("</div>")[0])
    # Get the launch description
    launchDescription = "%s"%(launch.split("missdescrip\">")[1].split("[")[0])
    launchCalHtml[launchCalHtml.index(launch)] = "%s\n\t%s\n\t%s\n\t%s"%(launchMission,launchWindow,launchSite,launchDescription)
  #print(type(launchCalHtml))
  return(launchCalHtml)

if __name__ == '__main__':
  launchCalHtml = grabRawPage("http")
  for launch in formatDataFromRawPage(launchCalHtml):
    print(launch)
