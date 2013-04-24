from celery import Celery
import subprocess
import shutil


celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def download(video_url):
    """Retrieve the file from the url"""
    destdir = 'files/{}/%(title)s.%(ext)s'.format(download.request.id)
    params = ['youtube-dl', video_url, '--output', destdir]
    subprocess.check_output(params)


@celery.task
def delete(task_id):
    """Delete the downloaded file with the given task_id"""
    rmdir = 'files/{}/'.format(task_id)
    shutil.rmtree(rmdir)
