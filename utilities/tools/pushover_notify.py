import http.client, urllib
import configparser

config = configparser.ConfigParser()

# Read the configuration file (this just needs to be relative to the top executable)
config.read('pushover_config.ini')
        
myApiKey    = config.get('config', 'myApiKey')
myUserKey   = config.get('config', 'myUserKey')
messageFile = config.get('config', 'messageFile')

with open(messageFile, "r") as fh_metrics:
    myMessage = ''.join(fh_metrics.readlines())

conn = http.client.HTTPSConnection("api.pushover.net:443")

conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": myApiKey,
    "user": myUserKey,
    "message": myMessage,
  }), { "Content-type": "application/x-www-form-urlencoded" })

thisResponse = conn.getresponse()

print(thisResponse.getcode())
