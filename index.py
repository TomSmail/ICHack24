from flask import Flask, send_from_directory, request, make_response
import os
from json import dumps
from model import solve
from calendar_generator import save_calendar, make_calendar

from convert import convert

PORT = os.environ["PORT"]

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World"

@app.route('/calculate_timetable', methods=['POST'])
def calculate_timetable():
    data = request.get_json()
    processed_data = convert(data["timetable_data"])
    name = str(data["file_id"])
    timetable = solve(processed_data)
    calendar = make_calendar(processed_data, timetable)
    save_calendar(calendar, name)
    print(f"Generated {name}.ics")
    return dumps({"url_path":f"https://ichack-e82c16304232.herokuapp.com/calendars/{name}.ics"})

@app.route('/calendars/<path:path>')
def send_report(path):
    response = make_response(send_from_directory('calendars', path))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

app.run(host='0.0.0.0', port=PORT)  
