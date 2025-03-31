from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from databases import Database
import httpx
from db_utils import DbUtils
from models import BaseJob, BaseMaintenanceTask, Job, MaintenanceTask, Robot, BaseRobot

db_provider = 'sqlite+aiosqlite:///./'
db_path = 'example.db'
db_url = db_provider + db_path

db = Database(db_url)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #setup
    print('Starting db setup')
    await db.connect()
    await db_utils.create_tables()
    print('Db setup complete')
    yield

    #teardown
    print('Disconnecting db...')
    await db.disconnect()
    print('Db disconnected')

app = FastAPI(lifespan=lifespan)
db_utils = DbUtils(db=db)

@app.get('/robots')
async def get_robots() -> list[Robot]:
    robots = await db_utils.get_robots()

    return robots

@app.get('/robots/{robot_id}')
async def get_robot(robot_id: int) -> Robot:
    robot = await db_utils.get_robot_by_id(robot_id)

    if robot is None:
        raise HTTPException(status_code=404, detail=f'Robot not found by id {robot_id}')
    else:
        return robot
    
@app.post('/robots')
async def add_robot(robot: BaseRobot) -> Robot:
    # first check existing
    robot_with_same_serial = await db_utils.get_robot_by_serial_number(robot.serial_number)

    if robot_with_same_serial is not None:
        return { 'error': f'Robot with serial number {robot.serial_number} already exists'}

    created_robot = await db_utils.create_robot(robot)

    print(f'Added a robot by serial number of {robot.serial_number}')
    return created_robot

@app.delete('/robots/{robot_id}')
async def delete_robot(robot_id: int):
    await db_utils.delete_robot(robot_id)

    print(f'Deleted a robot by id {robot_id}')

@app.get('/maintenance-tasks')
async def get_maintenance_tasks() -> list[MaintenanceTask]:
    tasks = await db_utils.get_maintenance_tasks()

    return tasks

@app.get('/maintenance-tasks/{task_id}')
async def get_maintenance_task(task_id: int) -> Robot:
    task = await db_utils.get_maintenance_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f'Task not found by id {task_id}')
    else:
        return task
    
@app.post('/maintenance-tasks')
async def add_maintenance_task(task: BaseMaintenanceTask) -> MaintenanceTask:
    task = await db_utils.create_maintenance_task(task)

    print(f'Added a task by id of {task.id}')
    return task

@app.delete('/maintenance-tasks/{task_id}')
async def delete_maintenance_task(task_id: int):
    await db_utils.delete_maintenance_task(task_id)

    print(f'Deleted a task by id {task_id}')

@app.get('/jobs')
async def get_jobs(robot_id: Optional[str] = Query(None, title="Robot id", description="Optional filter"), task_id: Optional[str] = Query(None, title="Task id", description="Optional filter")) -> list[Job]:
    tasks = await db_utils.get_jobs(robot_id, task_id)

    return tasks

@app.get('/jobs/{job_id}')
async def get_job(job_id: int) -> Job:
    job = await db_utils.get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail=f'Job not found by id {job_id}')
    else:
        return job
    
@app.post('/jobs')
async def add_job(job: BaseJob) -> Job:
    robot = await db_utils.get_robot_by_id(job.robot_id)
    if robot is None:
        raise HTTPException(status_code=404, detail=f"Robot not found by id {job.robot_id}")
    
    task = await db_utils.get_maintenance_task_by_id(job.task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found by id {job.task_id}")

    created_job = await db_utils.create_job(job)

    print(f'Added a job by id of {created_job.id}')
    return created_job

@app.delete('/jobs/{job_id}')
async def delete_job(job_id: int):
    await db_utils.delete_job(job_id)

    print(f'Deleted a job by id {job_id}')

@app.put('/jobs/{job_id}/status')
async def update_job_status(job_id: int, status: str) -> Job:
    updated_job = await db_utils.update_job_status(job_id, status)

    print(f'Updated job {job_id} to status of "{status}"')

    return updated_job

@app.post('/jobs/{job_id}/notify')
async def notify_job_details(job_id: int):
    job = await db_utils.get_job_by_id(job_id)
    robot = await db_utils.get_robot_by_id(job.robot_id)
    task = await db_utils.get_maintenance_task_by_id(job.task_id)

    data = {
        'job_id': job_id,
        'robot_id': robot.id,
        'task_id': task.id,
        'robot_name': robot.name,
        'task_name': task.name
    }

    notify_url = 'https://httpbin.org/post'

    async with httpx.AsyncClient() as client:
        response = await client.post(notify_url, json = data)
        json = response.json()

        print(f'Received response for job details notify of job {job_id}')
        print(json)