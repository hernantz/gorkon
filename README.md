GORKON
======
![Gorkon](http://fc09.deviantart.net/fs4/i/2004/221/b/7/Orc_Shaman.jpg)


Tiny webapp built on top of redis, celery, youtube-dl and flask that, provided
a youtube|vimeo|soundcloud|blip.tv link, will download the media file and
optionally convert the output to other format.


## TODO
* TESTS!!!1.
* Automated deployment.
* Use FlexBox for fun.
* Allow to queue multiple simultaneous downloads.
* Use celery [chains][chains]. Did not work when [tried][stackoverflow].
* Profit?


## INSTALL
For deploying and developing there are some fabric commands available.
For required users check fabhosts.py file.
All enviroment users must exist and all system packages must be installed.

**Installing required system wide packages**
* sudo apt-get update
* sudo apt-get install nginx python-pip gcc python-dev git virtualenvwrapper supervisor redis-server libav-tools

**Configuring fabric hosts**
The fabhosts.py file must contain the localhost, staging and production tasks to set up their respective
hosts enviroments. 
Examples of the env vars required are:

```python
@task
def localhost():
    env.hosts = ['localhost'],
    env.user = 'hernantz',
    env.folder = 'devel',
    env.project_name = 'gorkon'
    env.repo = 'https://github.com/hernantz/gorkon'
    env.project_path = '/home/%(user)s/%(folder)s/' % env
    env.src_path = '%(project_path)s%(project_name)s' % env
    env.static = '%(src_path)s/static' % env
    env.log_dir = '%(src_path)s/logs/' % env
    env.virtualenv_dir = '/home/%(user)s/.virtualenvs/%(project_name)s' % env
```

[chains]: http://docs.celeryproject.org/en/latest/userguide/canvas.html#chains "Celery chains documentation"
[stackoverflow]: http://stackoverflow.com/questions/16306175/get-progress-from-async-python-celery-chain-by-chain-id "Get progress from async python celery chain by chain id"
