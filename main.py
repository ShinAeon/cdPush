import os
from flask import Flask, request, jsonify, abort
from reminderJsonHElper import readReminderJson, writeReminderJson, createReminderJson
import uuid

app = Flask(__name__)

@app.route('/api/reminders', methods=['GET'])
def getReminders():
  reminders = readReminderJson()
  return jsonify({'reminders': reminders})

@app.route('/api/reminders', methods=['POST'])
def createReminder():
  req_data = request.get_json()

  if not all(item in req_data for item in ("phone_number", "message", "due_date")):
      abort(400)

  reminder = {
    'id': uuid.uuid4().hex,
    'phone_number': req_data['phone_number'],
    'message': req_data['message'],
    'due_date': req_data['due_date']
  }

  createReminderJson(reminder)
  return jsonify({'reminder': reminder}), 201


@app.errorhandler(400)
def badRequest(error):
  return jsonify({'error': 'Bad Request'}), 400

@app.route('/api/reminders/<reminder_id>', methods=['DELETE'])
def deleteReminder(reminder_id):
  reminders = readReminderJson()
  reminder = [reminder for reminder in reminders if reminder['id'] == reminder_id]
  if len(reminder) == 0:
    abort(404)
  reminders.remove(reminder[0])
  data = {}
  data['reminders'] = reminders
  writeReminderJson(data)
  return jsonify({'message': 'Reminder has been removed successfully'})

@app.errorhandler(404)
def not_found(error):
  return jsonify({'error': 'Not Found'}), 4046

if __name__ == '__main__':
    app.run()