from flask import Flask, render_template, request, send_file, \
    jsonify, url_for, redirect, session, abort
from forms import DownloadForm
from tasks import celery, download, delete, convert
from glob import glob
from redis import Redis
from redis_session import RedisSessionInterface
from celery import chain
from uuid import uuid1
import os


def file2dl(folder):
    """
    Check that the folder exists.
    Returns: file's name and location or 404 Not Found HTTP Response
    """
    d = 'files/{}/*'.format(folder)
    try:
        return os.path.basename(glob(d)[0]), glob(d)[0]
    except IndexError:
        abort(404)


def getnpop(var):
    """Retrieve var from session and remove it."""
    if var in session:
        return session.pop(var)


app = Flask(__name__)
redisconn = Redis(port=6380)
app.session_interface = RedisSessionInterface(redisconn)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DownloadForm(request.form)
    task = getnpop('task')  # are we processing a task already?

    if request.method == 'POST' and form.validate_on_submit():

        folder = str(uuid1())  # folder where to save the file

        # list of tasks to process
        tasks = [download.s(folder, form.video_url.data)]

        if form.convert.data in ('mp3', 'mp4'):
            # schedule file convertion to mp3 or mp4
            tasks.append(convert.s(form.convert.data))

        # start the chain and save the id in session for later ajax polling
        task_chain = chain(*tasks).apply_async()
        session['task'] = { "folder": folder, "task_id": task_chain.id }

        # schedule file removal in 30 min, whatever the result is
        delete.s(folder).set(countdown=980).apply_async()

        return redirect(url_for('index'))

    return render_template('index.html', form=form,
                           task=task)


@app.route('/check/<task_id>')
def check(task_id=None):
    """
    Given a task id, retrieve it's status
    and return a json response
    """
    task_chain = celery.AsyncResult(task_id)
    return jsonify(id=task_id, status=task_chain.status)


@app.route('/download/<folder>')
def dl(folder=None):
    # Get the filename and dir for the requested file
    filename, path = file2dl(folder)

    # Get some boilerplate headers from send_file()
    response = send_file(path)
    content_disposition = 'attachment; filename="{}"'.format(filename)
    response.headers['Content-Disposition'] = content_disposition
    x_accel_redirect = '/files/{0}/{1}'.format(folder, filename)
    response.headers['X-Accel-Redirect'] = x_accel_redirect
    return response


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
