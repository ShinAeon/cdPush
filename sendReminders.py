import os
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
  print(str(date.today()))
  print(reminders[0]['due_date'])
  if len(reminders_due) > 0:
    print('Dang')
    sendSMSReminder(reminders_due)


def sendSMSReminder(reminders):
  for reminder in reminders:
    twilio_from = os.getenv("TWILIO_SMS_FROM")
    to_phone_number = reminder['phone_number']
    twilioClient.messages.create(
      body=reminder['message'],
      from_=f"{twilio_from}",
      to=f"{to_phone_number}")
    updateDueDate(reminder)


def updateDueDate(reminder):
    reminders = readReminderJson()
    data = {}
    reminders.remove(reminder)
    new_due_date = datetime.strptime(
        reminder['due_date'], '%Y-%m-%d').date() + relativedelta(months=1)
    reminder['due_date'] = str(new_due_date)
    reminders.append(reminder)
    data['reminders'] = reminders
    writeReminderJson(data)


if __name__ == '__main__':
    findRemindersDue()