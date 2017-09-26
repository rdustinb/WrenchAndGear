# Libraries to access the MyIPAddress website
from urllib import request
from urllib import error

# Libraries to access the mail server
from smtplib import SMTP
from smtplib import SMTPHeloError
from smtplib import SMTPAuthenticationError
from smtplib import SMTPException

# Library for checking the stored IP File exists
from os import path
from os import getlogin

# Library for current date and time...always useful
from datetime import datetime, timezone

# Globals
# App-Specific Password for Google
MYPASSWORD = "ddcnwdelcvgonzre"
# Google Email Address
MYEMAIL = "embeddedcrypticvapor@gmail.com"
# This is the email that the update script "pretends" to send the email from
SERVEREMAIL = "terminalmail@server.com"
OLDIPLOG = "/Users/%s/Library/LaunchAgents/getExternalIP_storedip.log"%(getlogin())
ERRORIPLOG = "/Users/%s/Library/LaunchAgents/getExternalIP_errors.log"%(getlogin())
errorList = list()
receivedSMTPHeloError = False
receivedSMTPAuthenticationError = False
receivedSMTPException = False
receivedSMTPRecipientsRefused = False
receivedSMTPSenderRefused = False
receivedSMTPDataError = False

def getCurrentIp():
  ################################################################################
  # Try to access the External IP Website
  ################################################################################
  try:
    #return request.urlopen("https://myexternalip.com/raw").read().decode('utf-8').strip()
    return request.urlopen("https://wtfismyip.com/text").read().decode('utf-8').strip()
  except:
    errorList.append("A URLError occured when trying to access the wtfismyip website.")
    print("A URLError occured when trying to access the wtfismyip website.")

def checkStoredIp(ipaddress="127.0.0.1"):
  ################################################################################
  # Test for JSON File, Check Last Recorded IP Address
  ################################################################################
  if(errorList == []):
    # Only continue if the previous step has no errors
    storedipaddress = str()
    if(path.isfile(OLDIPLOG)):
      # If the storage file exists, read out the IP Address
      with open(OLDIPLOG, "r") as ipfh:
        for line in ipfh:
          storedipaddress = line
      # Compare stored IP Address with that just detected
      if(storedipaddress != ipaddress):
        with open(OLDIPLOG, "w") as ipfh:
          ipfh.write(ipaddress)
          sendUpdatedIp(ipaddress)
    else:
      # If no storage file exists, create it and the send an update email
      with open(OLDIPLOG, "w") as ipfh:
        ipfh.write(ipaddress)
        sendUpdatedIp(ipaddress)
  else:
    print("It looks like an error occured in getCurrentIp() so the function")
    print("checkStoredIp() is not being run...")

def sendUpdatedIp(ipaddress="127.0.0.1"):
  ################################################################################
  # Try to Login and Send update Email
  ################################################################################
  try:
    with SMTP('smtp.gmail.com:587') as email:
      email.starttls()
      email.login(MYEMAIL,MYPASSWORD)
      email.sendmail(SERVEREMAIL,MYEMAIL,
        "Subject: %s\n\nIP address has changed to:\n%s"%("Server IP Address",ipaddress))
  except SMTPHeloError:
    errorList.append("An SMTP Helo Error occurred.")
  except SMTPAuthenticationError:
    errorList.append("The server failed authentication.")
  except SMTPException:
    errorList.append("An unknown SMTP error occurred.")
  except SMTPRecipientsRefused:
    errorList.append("Delivery to all recipients failed.")
  except SMTPSenderRefused:
    errorList.append("The server rejected the from address.")
  except SMTPDataError:
    errorList.append("The server returned an unknown error.")

# Read and check
#getCurrentIp()
checkStoredIp(getCurrentIp())
# Store Errors to the Logfile
if(errorList != []):
  # Does this clear the file contents?
  with open(ERRORIPLOG, "w") as ipfh:
    pass
  # By opening it again?
  with open(ERRORIPLOG, "w") as ipfh:
    if(errorList != []):
      ipfh.write("Error list incurred the following errors:")
      for line in errorList:
        ipfh.write(line)
  # Let's also email when errors occur
  with SMTP('smtp.gmail.com:587') as email:
    email.starttls()
    email.login(MYEMAIL,MYPASSWORD)
    email.sendmail(SERVEREMAIL,MYEMAIL,
      "Subject: %s\n\nIP address update script had errors.\n%s"
      %("Update Script Errors",errorList))
