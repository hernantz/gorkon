from celery import Celery
import requests
import subprocess


celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def download(video_url):
    """Retrieve the file from the url"""
    subprocess.check_output(['youtube-dl', video_url, '--output', 'files/%(title)s.%(ext)s'])


@celery.task
def get_data(url):
    """Retrieve some data from file"""
    r = requests.get(url)
