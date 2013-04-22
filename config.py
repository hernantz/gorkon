import os


# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# secret key for session management and csrf
SECRET_KEY = 'lotr43vA'

DEBUG = True

# X-Sendfile feature for files sent with send_file()
USE_X_SENDFILE = True
