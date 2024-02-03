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
  
  sessions = {(day, sesh_num): (String(f'subject_{subject}'), String(f'task_{task}')) 
                for sesh_num in range(sessions_per_day)
                for day in range(num_days)
                for task in tasks
                for subject in subjects}
  
  # sessions_of_subject_task = {(subject, task): [(day, sesh_num)
  #                 for sesh_num in range(sessions_per_day)
  #                 for day in range(num_days)
  #               ]
  #               for task in tasks
  #               for subject in subjects}
  
  # sessions_per_task = {(subject, task): min_num_sessions, max_num_sessions}
  
  # only one subject and task per sesh_num
  # and match up sessions and task_at_session
  for (day, sesh_num, subject, task), doing_task in task_at_session.items():
    constraints.append((sessions[day, sesh_num] == (subject, task)) == doing_task)
    # constraints.append(PbLe([(task_at_session[()], 1) , 1))
    
  # for (subject, task), num_sessions in min_num_sessions_per_subject_task:
    
  # for (subject, task), day_session_lst in sessions_of_subject_task:
  #   constraints.append(subjects[subject][task].first <= len(day_session_lst))
  #   constraints.append(subjects[subject][task].second >= len(day_session_lst))
    
  for subject in subjects:
      for task in tasks[subject]:
        # day_session_lst =
        constraints.append(PbLe([(task_at_session[(day, sesh_num, subject, task)], 1) for sesh_num in range(sessions_per_day) for day in range(num_days)], subjects[subject][task].first))


def solve(input_data, optimise=False, timeout=120, out=True):
    constraints, variables = build_constraints(input_data)
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
        
    if out:
      print(m["sessions"])

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

    
  

  
  
    
    