from celery import Celery, current_task
import subprocess


celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def download(video_url, task_id=None):
    """Retrieve the file from the url"""
    destdir = 'files/{}/%(title)s.%(ext)s'.format(download.request.id)
    params = ['youtube-dl', video_url, '--output', destdir]
    subprocess.check_output(params)
