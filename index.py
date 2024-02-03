from flask import Flask, send_from_directory
import os
PORT = os.environ["PORT"]

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World"

@app.route('/calendars/<path:path>')
def send_report(path):
    return send_from_directory('calendars', path)

app.run(host='0.0.0.0', port=PORT, debug=True)  
# {
# 	"session_length": 1,
#   "start_time": "9:00",
#   "end_time": "13:00",
#   "subjects": [
# 	   "maths": [
#          "notes": {
#             "min_time": 10,
#             "max_time": 20
#          }
#          "textbook": ...
#          "past papers": ...
#       ]
#   ]
# }