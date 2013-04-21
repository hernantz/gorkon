from flask import Flask, render_template, request
from forms import DownloadForm
from tasks import download


app = Flask(__name__)
app.config.from_object('config')


@app.route("/", methods=['GET', 'POST'])
def index():
    form = DownloadForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        task = download.delay(form.video_url.data)
        return render_template('index.html', form=form, task_id=task.id)
    return render_template('index.html', form=form)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
