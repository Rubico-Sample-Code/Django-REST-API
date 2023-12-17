# tasks.py
from celery import shared_task
import subprocess

@shared_task
def run_django_command_with_id_task(command_name, id):
    try:
        command = ['python', 'manage.py', command_name, str(id)]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
    except Exception as e:
        return str(e)
