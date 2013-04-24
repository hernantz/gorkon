import os


# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# secret key for session management and csrf
SECRET_KEY = os.urandom(20)

DEBUG = True
