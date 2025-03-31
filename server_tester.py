from datetime import date, timedelta
import requests

base_url = 'http://localhost:8000/'
custom_part = 'jobs?robot_id=3'

url = base_url + custom_part

tomorrow = date.today() + timedelta(days=1)

robot_data = {
    'name': 'Robo Mobo Alpha',
    'model': 'Good 0.9',
    'serial_number': 'ISO_MISO_SCHMISO_6000'
}

task_data = {
    'name': 'Wash dishes',
    'description': 'just do it',
    'frequency': 4
}

job_data = {
    'robot_id': 1,
    'task_id': 1,
    'due_date': tomorrow.isoformat()
}

response = requests.get(url)
json = response.json()

print(json)