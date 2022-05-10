import os
import random
from reminderJsonHElper import readReminderJson, writeReminderJson
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv

load_dotenv()

proxyClient = TwilioHttpClient(proxy={
  'http': os.getenv("http_proxy"), 
  'https': os.getenv("https_proxy")
})

twilioClient = Client(http_client=proxyClient)

def findRemindersDue():
  reminders = readReminderJson()
  reminders_due = [
    reminder for reminder in reminders if reminder['due_date'] == str(date.today())
  ]
  if len(reminders_due) > 0:
    sendSMSReminder(reminders_due)

def sendSMSReminder(reminders):
  for reminder in reminders:
    twilio_from = os.getenv("TWILIO_SMS_FROM")
    to_phone_number = reminder['phone_number']
    twilioClient.messages.create(
      body=reminder['message'],
      from_=f"{twilio_from}",
      to=f"{to_phone_number}")

def checkForSunday():
  return datetime.today().weekday() == 6

def pickNewChallengeDay():
  delta = random.randrange(1, 8)
  return datetime.today().date() + relativedelta(days=delta)

def addNextChallenge(date):
  reminders = readReminderJson()
  data = {}
  reminders.clear()
  reminder = {
    "phone_number": "+17192291307",
    "message": "It's challenge day!!! Get your act together and OWN THIS ONE!!!",
    "due_date": ""
  }
  reminder['due_date'] = str(date)
  reminders.append(reminder)
  data['reminders'] = reminders
  writeReminderJson(data)

if __name__ == '__main__':
    findRemindersDue()
    if checkForSunday():
      addNextChallenge(pickNewChallengeDay())