from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
program = FastAPI()

entries = {
    1:{
        "Task": "Shid",
        "Description": "Take a massive Dump.",
        "Time": 15
    },
    2:{
        "Task": "Piss",
        "Description": "Urinate until bladder dry.",
        "Time": 2
    },
    3: {
        "Task": "Cry",
        "Description": "Every man cries internally.",
        "Time required in minutes": 60
    },
    4: {
        "Task": "Repeat",
        "Description": "Finally the Vicious Cycle of life.",
        "Time": 2
    }
}

class Tasks(BaseModel):
    Task : str
    Description : str
    Time : int

class UpdateTasks(BaseModel):
    Task : Optional[str] = None
    Description : Optional[str] = None
    Time : Optional[int] = None

@program.get("/")
def function():
    return "HellO"

@program.get("/welcome/")
def welcome(name: str, lastname: str):
    return f"Welcome  {name} {lastname}"

@program.get("/number_of_tasks")
def number_of_tasks():
    return len(entries)

@program.get("/get_Task_number/{entry}")
def get_Task_number(entry: int = Path(None, description = "Enter the Task number required:")):
    if entry > len(entries):
        return "Entry doesn't Exist"
    return entries[str("Task"+str(entry))]

@program.get("/get_all_tasks")
def get_all_tasks():
    return entries

@program.post("/create_task")
def create_task(task_number :int, task_desc : Tasks):
    if task_number in entries:
        return {"Error" : "Task Exists"}
    entries[task_number] = task_desc
    return entries[task_number]

@program.put("/update_task")
def update_task(task_number :int, update_desc : UpdateTasks):
    if task_number not in entries:
        return {"Error" : "Task does not Exist"}

    if update_desc.Task != None:
        entries[task_number]["Task"] = update_desc.Task

    if update_desc.Description != None:
        entries[task_number]["Description"] = update_desc.Description

    if update_desc.Time != None:
        entries[task_number]["Time"] = update_desc.Time

    return entries[task_number]

@program.delete("/delete_task")
def delete_task(task_number :int):
    if task_number not in entries:
        return "Task doesn't exist"
    entries.pop(task_number)
    return "Task removed successfully"
