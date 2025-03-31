from datetime import date
from pydantic import BaseModel

class BaseRobot(BaseModel):
    name: str
    model: str
    serial_number: str

class Robot(BaseRobot):
    id: int

class BaseMaintenanceTask(BaseModel):
    name: str
    description: str
    frequency: int

class MaintenanceTask(BaseMaintenanceTask):
    id: int

class BaseJob(BaseModel):
    robot_id: int
    task_id: int
    due_date: date

class Job(BaseJob):
    id: int
    status: str