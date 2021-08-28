from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
import mongoengine as db
program = FastAPI()
db.connect("MongoFastAPI")


class Todo(db.Document):
    entry_no = db.IntField()
    task = db.StringField()
    description = db.StringField()
    time = db.IntField()


    def to_json(self):
        return {
            self.entry_no:
            {
                "Task": self.task,
                "Description": self.description,
                "Time required in minutes": self.time
             }
        }

class Tasks(BaseModel):
    entry_no: int
    Task: str
    Description: str
    Time: int

class UpdateTasks(BaseModel):
    Task: Optional[str] = None
    Description: Optional[str] = None
    Time: Optional[int] = None

@program.get("/")
def function():
    return "Hello"

@program.get("/welcome/")
def welcome(name: str, lastname: str):
    return f"Welcome  {name} {lastname}"

@program.get("/todo_count")
def number_of_tasks():
    return Todo.objects.count()

@program.get("/todo/{entry}")
def get_Task_number(entry: int = Path(None, description="Enter the Task number required:")):
    if entry > Todo.objects.count():
        return "Entry doesn't Exist"
    task = Todo.objects(entry_no=entry).first()
    return task

@program.get("/todo")
def get_all_tasks():
    task_list = []
    for item in Todo.objects():
        task_list.append(item.to_json())
    return task_list

@program.get("/todo_delete")
def delete_database():
    for task in Todo.objects():
        task.delete()
    return "Done"

@program.post("/todo")
def create_task(task_number: int, task_desc: Tasks):
    todo = Todo(
        entry_no=task_desc.entry_no,
        task=task_desc.Task,
        description=task_desc.Description,
        time=task_desc.Time
    )
    todo.save()
    return "Created"

@program.put("/todo")
def update_task(task_number: int, update_desc: UpdateTasks):
    task_obj = Todo.objects(entry_no=task_number).first()

    if update_desc.Task != None:
        task_obj.update(task=str(update_desc.Task))

    if update_desc.Description != None:
        task_obj.update(description=str(update_desc.Description))

    if update_desc.Time != None:
        task_obj.update(time=str(update_desc.Time))

    return "Updated"

@program.delete("/todo")
def delete_task(task_number: int):
    task_obj = Todo.objects(entry_no=task_number).first()
    task_obj.delete()
    return "Deleted"
