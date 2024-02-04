import icalendar as ic
from datetime import date
from string import ascii_lowercase
import datetime
import os
DEBUG = False
def convert_json_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
def get_daily(timetable, target_day):
    got = {}
    for ((daynum, snum),v) in timetable.items():
        if daynum == target_day:
            if snum in got:
                ### ERROR
                pass
            else:
                got[snum] = v
    return got

def make_calendar(processed_data, timetable):
    calendar = ic.Calendar()

    calendar.add("x-wr-calname", "Study Timetable")
    calendar.add("last-modified", datetime.datetime.now())

    num_sessions = processed_data["sessions_per_day"]
    session_length = processed_data["session_length"]
    start_date = processed_data["start_date"]
    end_date = processed_data["end_date"]
    number_of_days = processed_data["number_of_days"]


    for calday in range(number_of_days):
        for snum in range(num_sessions):
            e = ic.Event()
            if (calday, snum) in timetable:
                subject, task = timetable[calday, snum]
                # subject,task = "Maths", "Notes"
                event_start = start_date+datetime.timedelta(days=calday, hours=snum*session_length)
                event_end = start_date+datetime.timedelta(days=calday, hours=(1+snum)*session_length)
                e.add("summary", f"Subject: {subject} and task: {task}")
                e.add("dtstart", event_start)
                e.add("dtend", event_end)
                if DEBUG:
                    print(f"Generated event {subject} task: {task} at {event_start} until {event_end} on (day:{calday}, session_num{snum})")
                calendar.add_component(e)
    return calendar

def save_calendar(calendar, name):
    f = open(os.path.join("calendars", f"{name}.ics"), "wb")
    f.write(calendar.to_ical())
    f.close()

if __name__ == "__main__":
    from random import randint
    import model
    DEBUG = True
    tlist = []
    for i in range(3):

        tasks = {"notes": [randint(1,5), randint(5,7)], "past papers": [randint(1,5), randint(5,7)], "textbook": [randint(1,5), randint(5,7)]}
        tlist.append(tasks)
    processed_example = {"session_length": 1.5,
                         "start_date": datetime.datetime(year=2024, month=2, day=2, hour=9),
                         "end_date": datetime.datetime(year=2024, month=2, day=2, hour=9)+ datetime.timedelta(days=7),
                         "number_of_days": 10,
                         "sessions_per_day": 4,
                         "subjects": ["Maths", "Physics", "French"],
                         "tasks": {"Maths": tlist[0], "Physics": tlist[1], "French": tlist[2]},
                         "possible_tasks": ["notes", "textbook", "past papers"]
                         }

    result = model.solve(processed_example)
    tc = make_calendar(processed_example, result)

    save_calendar(tc, "blah")
