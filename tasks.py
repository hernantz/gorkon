from celery import Celery
import subprocess
import shutil
from glob import glob
import os


celery = Celery('tasks')
celery.config_from_object('celeryconfig')


def change_ext(inputfile, ext):
    """Shifts file extensions"""
    filename, old_ext = os.path.splitext(inputfile)
    return '.'.join([filename, ext])


@celery.task
def download(folder, video_url):
    """Retrieve the file from the url"""
    destdir = 'files/{}/%(title)s.%(ext)s'.format(folder)
    params = ['youtube-dl', video_url, '--output', destdir]
    subprocess.check_output(params)
    return folder  # stupid celery forces me to return this to group tasks


@celery.task
def convert(folder, fmt):
    """Convert the downloaded file to mp3|mp4 with the given folder"""
    inputfile = glob('files/{}/*'.format(folder))[0]  # get input filename
    outputfile = change_ext(inputfile, fmt)  # build the output filename

    # perform convertion and delete inputfile if needed
    if (inputfile != outputfile):
        subprocess.check_output(['avconv', '-i', inputfile, outputfile])
        os.remove(inputfile)


@celery.task
def delete(folder):
    """Delete the downloaded file with the given folder"""
    rmdir = 'files/{}/'.format(folder)
    shutil.rmtree(rmdir)
