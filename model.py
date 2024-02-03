import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List
import datetime

# from input_validator import validate_input
import os

from z3 import *


example_dict = {'session_length': 1.5, 'start_date': datetime.datetime(2024, 2, 3, 20, 54, 57, 508914), 'end_date': datetime.datetime(2024, 2, 10, 20, 54, 57, 508914), 'number_of_days': 5, 'sessions_per_day': 4, 'subjects': ['Maths', 'Physics', 'French'], 'possible_tasks': ['notes', 'past papers', 'textbook'], 'tasks': {'Maths': {'notes': [5, 6], 'past papers': [2, 5], 'textbook': [2, 7]}, 'Physics': {'notes': [1, 6], 'past papers': [5, 7], 'textbook': [3, 6]}, 'French': {'notes': [5, 5], 'past papers': [4, 6], 'textbook': [4, 7]}}}

def build_constraints(input_data: Dict[str, Any]):

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



  return constraints


def solve(input_data, optimise=False, timeout=120, out=True):
    constraints = build_constraints(input_data)
    m = None
    if not optimise:
        solver = Solver()
        solver.set(timeout=timeout*1000)
        solver.add(constraints)
        if solver.check() == unsat:
            if out:
                print("No plan possible")
            return None
        if solver.reason_unknown() == "timeout":
            raise TimeoutError
        m = solver.model()

        ### Builds (day, seshnum):(subject, task)



# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("input_file", help="JSON file describing problem to be solved.", type=Path)
#     parser.add_argument("--timeout", default=60, help="Maximum time allowed for SMT solving.",
#                         type=int)
#     parser.add_argument("--opt", action="store_true", help="Find optimal plan.")
#     args = parser.parse_args()

#     input_file: Path = args.input_file
#     optimise = args.opt
#     timeout: int = args.timeout

#     if timeout <= 0:
#         print(f"Timeout value must be positive; got {timeout}.")
#         sys.exit(1)
#     if not input_file.is_file():
#         print(f"The provided input file {input_file} does not exist.")
#         sys.exit(1)

#     input_data = validate_input(input_file)
#     if input_data is None:
#         sys.exit(1)
#     try:
#         solve(input_data, optimise, timeout)
#     except TimeoutError:
#         print("Computing a plan timed out")
#         sys.exit(1)


if __name__ == "__main__":
    solve(example_dict)







