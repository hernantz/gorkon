from flask import Flask, render_template, request, send_file, \
                  jsonify, url_for, redirect, session, flash
from forms import DownloadForm
from tasks import download
from glob import glob
from redis_session import RedisSessionInterface


def file2dl(task_id):
    """
    Check that the task_id's file exists.
    Returns: file location or None
    """
    d = 'files/{}/*'.format(task_id)
    try:
       return glob(d)[0]
    except IndexError:
        return None


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
    return send_file(file2dl(task_id))


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
