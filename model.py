import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List
import datetime

# from input_validator import validate_input
import os

from z3 import *


example_dict = {'session_length': 1.5, 'start_date': datetime.datetime(2024, 2, 3, 20, 54, 57, 508914), 'end_date': datetime.datetime(2024, 2, 10, 20, 54, 57, 508914), 'number_of_days': 10, 'sessions_per_day': 4, 'subjects': ['Maths', 'Physics', 'French'], 'possible_tasks': ['notes', 'past papers', 'textbook'], 'tasks': {'Maths': {'notes': [5, 6], 'past papers': [2, 5], 'textbook': [2, 7]}, 'Physics': {'notes': [1, 6], 'past papers': [5, 7], 'textbook': [3, 6]}, 'French': {'notes': [5, 5], 'past papers': [4, 6], 'textbook': [4, 7]}}}

def build_constraints(input_data: Dict[str, Any], reduce_factor):

  constraints = []
  subjects = input_data["subjects"]
  tasks = input_data["tasks"]

  possible_tasks = input_data["possible_tasks"]
  sessions_per_day = input_data["sessions_per_day"]
  num_days = input_data["number_of_days"]
  # num_sessions_per_subject = input_data["num_sessions_per_subject"]
  # max_num_sessions_per_subject_task = input_data["max_num_sessions_per_subject_task"]

  task_at_session = {(day, sesh_num, subject, task): Bool(f'{subject}_{task}_at_{sesh_num}_of_day_{day}')
                for sesh_num in range(sessions_per_day)
                for day in range(num_days)
                for task in possible_tasks
                for subject in subjects
  }
  ### For every (day, sesh_num) atMost 1 of [(day, seshnum, subject, task) for each subject and task]
  ### for every (subject, task) we want at least tasks[min] and at most tasks[max] over all days and sesh_nums z3.Sum
  ### rotation of subjects

  for day in range(num_days):
      for sesh_num in range(sessions_per_day):
          doing = []
          for subject in subjects:
              for task in possible_tasks:
                  doing.append(task_at_session[(day, sesh_num, subject, task)])


          constraints.append(AtMost(*doing, 1))
  for subject in subjects:
    for task in possible_tasks:
      doing = []
      for day in range(num_days):
        for sesh_num in range(sessions_per_day):
          doing.append(task_at_session[(day, sesh_num, subject, task)])

      mi,ma = tasks[subject][task]
      constraints.append(AtLeast(*doing, int(reduce_factor * mi)))
      constraints.append(AtMost(*doing, int(reduce_factor * ma)))


  return constraints


def solve(input_data, timeout=120, out=True):
    subjects = input_data["subjects"]
    possible_tasks = input_data["possible_tasks"]
    sessions_per_day = input_data["sessions_per_day"]
    num_days = input_data["number_of_days"]

    m = None
    is_sat = False
    reduce_factor = 1
    while True:
        constraints = build_constraints(input_data, reduce_factor)
        solver = Solver()
        solver.set(timeout=timeout*1000)
        solver.add(constraints)
        is_sat = solver.check()
        if solver.reason_unknown() == "timeout":
            raise TimeoutError
        if (is_sat):
            break
        reduce_factor -= 0.1



    m = solver.model()

    ### Builds (day, seshnum):(subject, task)
    timetable = {}
    for day in range(num_days):
        for sesh_num in range(sessions_per_day):
            for subject in subjects:
                for task in possible_tasks:
                    if m[Bool(f'{subject}_{task}_at_{sesh_num}_of_day_{day}')]:
                        timetable[day, sesh_num] = (subject, task)

    return timetable



if __name__ == "__main__":
    solve(example_dict)







