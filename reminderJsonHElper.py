import os
import json

fileName = 'reminder.json'
reminderTag = 'reminders'

def reminderJsonExists():
  return os.path.isfile(fileName)


def readReminderJson():
  if reminderJsonExists():
    with open(fileName) as reminder_json:
      data = json.load(reminder_json)
      return data[reminderTag]
  else:
    return {}


def createReminderJson(reminder):
  if not reminderJsonExists():
    data = {}
    data[reminderTag] = []
    data[reminderTag].append(reminder)
    writeReminderJson(data)
  else:
    updateReminderJson(reminder)


def updateReminderJson(reminder):
  with open(fileName) as reminder_json:
    data = json.load(reminder_json)
    reminders = data[reminderTag]
    reminders.append(reminder)
    writeReminderJson(data)


def writeReminderJson(data, filename=fileName):
  with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=4)