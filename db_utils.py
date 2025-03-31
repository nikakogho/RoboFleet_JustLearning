from databases import Database
from models import BaseJob, BaseMaintenanceTask, BaseRobot, Job, MaintenanceTask, Robot

class DbUtils:
    def __init__(self, db: Database):
        self.db = db

    async def create_tables(self):
        robots_create = """CREATE TABLE IF NOT EXISTS Robots (id INTEGER Primary Key, name varchar(100), model varchar(100), serial_number INTEGER unique)"""

        await self.db.execute(robots_create)

        standard_maintenance_create = """CREATE TABLE IF NOT EXISTS StandardMaintenanceTasks (id INTEGER Primary Key, name varchar(100), description varchar(500), frequency INTEGER)"""

        await self.db.execute(standard_maintenance_create)

        jobs_create = """CREATE TABLE IF NOT EXISTS Jobs (
            id INTEGER Primary Key,
            robot_id INTEGER,
            task_id INTEGER,
            due_date DATE,
            status TEXT DEFAULT 'New',
            FOREIGN KEY (robot_id) REFERENCES Robots (id),
            FOREIGN KEY (task_id) REFERENCES StandardMaintenanceTasks (id)
        )"""

        await self.db.execute(jobs_create)

    async def get_robots(self) -> list[Robot]:
        query = """SELECT * FROM Robots"""

        return await self.db.fetch_all(query)
    
    async def get_robot_by_id(self, id: int) -> Robot:
        query = """SELECT * FROM Robots WHERE id = :id"""
        robot = await self.db.fetch_one(query, values={"id": id})

        return robot
    
    async def get_robot_by_serial_number(self, serial_number: str) -> Robot:
        existing_query = """SELECT * FROM Robots WHERE serial_number = :serial_number"""
        robot = await self.db.fetch_one(existing_query, values={'serial_number': serial_number})

        return robot
    
    async def create_robot(self, robot: BaseRobot) -> Robot:
        add_query = """INSERT INTO Robots (name, model, serial_number) VALUES (:name, :model, :serial_number)"""
        values = {
            "name": robot.name,
            "model": robot.model,
            "serial_number": robot.serial_number
        }

        created_id = await self.db.execute(add_query, values)

        return await self.get_robot_by_id(created_id)
    
    async def delete_robot(self, id: int):
        query = """DELETE Robots WHERE id = :id"""
        
        await self.db.execute(query, values={"id": id})

    async def create_maintenance_task(self, task: BaseMaintenanceTask) -> MaintenanceTask:
        add_query = """INSERT INTO StandardMaintenanceTasks (name, description, frequency) VALUES (:name, :description, :frequency)"""
        values = {
            "name": task.name,
            "description": task.description,
            "frequency": task.frequency
        }

        created_id = await self.db.execute(add_query, values)

        return await self.get_maintenance_task_by_id(created_id)
    
    async def get_maintenance_tasks(self) -> list[MaintenanceTask]:
        query = """SELECT * FROM StandardMaintenanceTasks"""

        return await self.db.fetch_all(query)
    
    async def get_maintenance_task_by_id(self, id: int) -> Robot:
        query = """SELECT * FROM StandardMaintenanceTasks WHERE id = :id"""
        task = await self.db.fetch_one(query, values={"id": id})

        return task
    
    async def delete_maintenance_task(self, id: int):
        query = """DELETE StandardMaintenanceTasks WHERE id = :id"""
        
        await self.db.execute(query, values={"id": id})

    async def create_job(self, job: BaseJob) -> Job:
        add_query = """INSERT INTO Jobs (robot_id, task_id, due_date) VALUES (:robot_id, :task_id, :due_date)"""
        values = {
            "robot_id": job.robot_id,
            "task_id": job.task_id,
            "due_date": job.due_date
        }

        created_id = await self.db.execute(add_query, values)

        return await self.get_job_by_id(created_id)
    
    async def get_jobs(self, robot_id: int | None, task_id: int | None) -> list[Job]:
        query = """SELECT * FROM Jobs"""
        values = {}

        if robot_id is not None or task_id is not None:
            query += " WHERE"

            if robot_id is not None:
                query += " robot_id = :robot_id"
                values['robot_id'] = robot_id
            
            if robot_id is not None and task_id is not None:
                query += " AND"

            if task_id is not None:
                query += " task_id = :task_id"
                values['task_id'] = task_id

        return await self.db.fetch_all(query, values=values)
    
    async def get_job_by_id(self, id: int) -> Job:
        query = """SELECT * FROM Jobs WHERE id = :id"""
        job = await self.db.fetch_one(query, values={"id": id})

        return job
    
    async def delete_job(self, id: int):
        query = """DELETE Jobs WHERE id = :id"""
        
        await self.db.execute(query, values={"id": id})

    async def update_job_status(self, id: int, new_status: str) -> Job:
        query = """UPDATE Jobs SET status = :new_status WHERE id = :id"""
        values = {
            'new_status': new_status,
            'id': id
        }

        await self.db.execute(query, values=values)

        return await self.get_job_by_id(id)
