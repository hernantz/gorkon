from flask.ext.wtf import Form, TextField
from wtforms.validators import Required, Length, URL
from urlparse import urlparse


VALID_SITES = ['youtube.com', 'www.youtube.com',
               'vimeo.com', 'www.vimeo.com',
               'soundcloud.com', 'www.soundcloud.com']


class DownloadForm(Form):
    video_url = TextField('Video URL', validators=[
        Required(), Length(min=6, max=500), URL()])

    def validate(self):
        """Check also that the url is from the supported sites"""
        rv = Form.validate(self)
        if not rv:
            return False

        # Get the elements of the url
        parsed_url = urlparse(self.video_url.data)

        if parsed_url.hostname not in VALID_SITES:
            self.video_url.errors.append('Not supported site.')
            return False

        return True
