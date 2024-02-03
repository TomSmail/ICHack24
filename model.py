import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

# from input_validator import validate_input
import os

from z3 import *

# def 
# z3

# x = Int('x')
# y = Int('y')
# solve(x > 2, y < 10, x + 2*y == 7)
def sessions_per_day(json_data: Dict[str, Any]):
  return 8

def build_constraints(json_data: Dict[str, Any]):
  
  constraints = []
  subjects = json_data["subjects"]
  tasks = json_data["tasks"]
  sessions_per_day = sessions_per_day(json_data)
  num_days = num_days(json_data)
  min_num_sessions_per_subject_task = json_data["num_sessions_per_subject_task"]
    
  task_at_session = {(day, sesh_num, subject, task): Bool(f'{subject}_{task}_at_{sesh_num}_of_day_{day}') 
                for sesh_num in range(sessions_per_day)
                for day in num_days
                for task in tasks
                for subject in subjects}
  
  sessions = {(day, sesh_num): (subject, task) 
              for 
  
  sessions_of_subject_task = {(subject, task): [day, sessions]}
  
  sessions_per_task = {(subject, task): min_num_sessions, max_num_sessions}
  
  # only one subject and task per sesh_num
  # and match up sessions and task_at_session
  for (day, sesh_num, subject, task), doing_task in task_at_session.items():
    constraints.append((sessions[day, sesh_num] == (subject, task)) == doing_task)
    # constraints.append(PbLe([(task_at_session[()], 1) , 1))
    
  for (subject, task), num_sessions in min_num_sessions_per_subject_task:
    
  for (subject, task) day_sessions_lst in sessions_of_subject_task:
    constraints.append(min_num_sessions_per_subject_task[(subject, task)] <= len(day_session_lst))
    constraints.append(max_num_sessions_per_subject_task[(subject, task)] => len(day_session_lst))
    
    
  

  
  
    
    