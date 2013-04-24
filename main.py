from flask import Flask, render_template, request, send_file, \
                  jsonify, url_for, redirect, session, abort
from forms import DownloadForm
from tasks import download
from glob import glob
import os
from redis_session import RedisSessionInterface


def file2dl(task_id):
    """
    Check that the task_id's file exists.
    Returns: file's name and location or 404 Not Found HTTP Response
    """
    d = 'files/{}/*'.format(task_id)
    try:
        return os.path.basename(glob(d)[0]), glob(d)[0]
    except IndexError:
        abort(404)


def getnpop(var):
    """Retrieve var from session and remove it."""
    if var in session:
       return session.pop(var)


app = Flask(__name__)
app.session_interface = RedisSessionInterface()
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = DownloadForm(request.form)
    task = getnpop('task')
    if request.method == 'POST' and form.validate_on_submit():
        session['task'] = download.delay(form.video_url.data)
        return redirect(url_for('index'))
    return render_template('index.html', form=form, task=task)


@app.route('/check/<task_id>')
def check(task_id=None):
    result = download.AsyncResult(task_id)
    return jsonify(id=task_id, status=result.status,
                   link=url_for('dl', task_id=task_id))


@app.route('/download/<task_id>')
def dl(task_id=None):
    filename, path = file2dl(task_id)  # Get the filename and dir for the requested file
    response = send_file(path)  # Get some boilerplate headers from send_file()
    response.headers['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    response.headers['X-Accel-Redirect']= '/files/{0}/{1}'.format(task_id, filename)
    return response


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
