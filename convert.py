from datetime import datetime
from typing import List, Dict, Any


def get_datetime(date: str, time: str) -> datetime:
    start_datetime = date + time
    return datetime.strptime(start_datetime, "%Y-%m-%d%H:%M")


def get_total_days(start: str, end: str) -> int:
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    return (end_date - start_date).days


def session_per_day(start: str, end: str, session_len: float) -> int:
    start_time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    total_time = end_time - start_time
    return int((total_time.total_seconds() / 3600) // session_len)


def process_activities(subjects: List[Dict[str, Any]]) -> Dict[str, Any]:
    processed_dic = dict()
    for subject in subjects:
        activity_dic = dict()
        for activity in subject["activities"]:
            activity_dic[activity["name"]] = (activity["min_time"], activity["max_time"])

        processed_dic[subject["name"]] = activity_dic
    return processed_dic


def convert(json_data: Dict[str, Any]) -> Dict[str, Any]:
    processed_data = dict()
    processed_data["session_length"] = json_data["session_length"]
    processed_data["start_date"] = get_datetime(json_data["start_date"], json_data["start_time"])
    processed_data["end_date"] = get_datetime(json_data["end_date"], json_data["end_time"])
    processed_data["number_of_days"] = get_total_days(json_data["start_date"], json_data["end_date"])
    processed_data["sessions_per_day"] = session_per_day(json_data["start_time"], json_data["end_time"],
                                                         json_data["session_length"])
    subjects = process_activities(json_data["subjects"])
    processed_data["subjects"] = list(subjects.keys())
    processed_data["tasks"] = subjects
    return processed_data


# processed_data: Dict[str, Any] = {
# session_length: float,
# start_date: datetime, ### Combines start date and start time
# end_date: datetime, ### Same as above
# number_of_days: int,
# session_per_day: int,
# subjects: List[str],
# tasks: Dict[subject_name: Dict[task_name:(min_num, max_num)]]}

if __name__ == "__main__":
    jsonfile = {"start_date": "2023-08-05", "end_date": "2023-08-15", "start_time": "9:00", "end_time": "14:00",
                "session_length": 0.5, "subjects":
                    [{"name": "maths", "activities": [{"name": "notes", "min_time": 10.0, "max_time": 20.0},
                                                      {"name": "past_paper", "min_time": 10.0, "max_time": 30.0}]},
                     {"name": "computer science", "activities": [{"name": "notes", "min_time": 10.0, "max_time": 20.0},
                                                                 {"name": "lectures", "min_time": 20.0,
                                                                  "max_time": 30.0}]}
                     ]}

    processed = convert(jsonfile)
    print(processed)
