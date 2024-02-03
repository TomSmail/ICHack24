from flask import Flask, send_from_directory
import os
from json import dumps

PORT = os.environ["PORT"]

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World"

@app.route('/calculate_timetable', methods=['POST'])
def calculate_timetable():
    content = request.get_json()
    print(content['file_id'])
    return dumps({"locale":"fr-FR"})

@app.route('/calendars/<path:path>')
def send_report(path):
    return send_from_directory('calendars', path)

app.run(host='0.0.0.0', port=PORT)  
