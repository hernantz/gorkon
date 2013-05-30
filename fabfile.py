from fabric.api import task, sudo, run, prefix, env, cd, settings
from fabric.utils import abort
from fabric.contrib.files import upload_template, first, exists
from contextlib import contextmanager, nested
import os


try:
    # include hosts envs
    from fabhosts import localhost, staging, production
except ImportError:
    abort("No fabhosts.py found!")


def once(s):
    "Command_prefixes is a list of prefixes"
    if s not in env.command_prefixes:
        return s
    return 'true'


@contextmanager
def vwrap():
    """Activates virtualenvwrapper commands"""
    # This is the location if installed via:
    # apt-get install virtualenvwrapper
    shfile = first('/etc/bash_completion.d/virtualenvwrapper',
                   '/usr/local/bin/virtualenvwrapper.sh')
    with prefix(once('source %s' % shfile)):
        yield


@contextmanager
def virtualenv():
    with nested(vwrap(), prefix(once('workon %s' % env.project_name))):
        yield


@contextmanager
def cd_project_path():
    """Cd one folder above the src folder"""
    with cd(env.project_path):
        yield


@contextmanager
def cd_src_path():
    """Cd inside the src folder"""
    with cd(env.src_path):
        yield


@task
def mkvirtualenv():
    """Just create a virtual enviroment"""
    if not exists(env.virtualenv_dir):
        with nested(vwrap(), settings(warn_only=True)):
            run('mkvirtualenv %(project_name)s' % env)


def reload_nginx():
    sudo('service nginx reload')


def reload_supervisord():
    sudo('supervisorctl update gorkon:*')
    sudo('supervisorctl restart gorkon:*')


def _config(src, dst):
    with cd_src_path():
        upload_template(src, dst, context=env, use_sudo=True,
                        use_jinja=True, backup=False)


def config_redis():
    _config('configfiles/redis.conf', '/etc/redis/gorkon.conf')


def config_supervisord():
    _config('configfiles/supervisor.conf', '/etc/supervisor/conf.d/gorkon.conf')


def config_nginx_site():
    _config('configfiles/nginx.conf', '/etc/nginx/sites-enabled/gorkon.conf')


@task
def install_requirements():
    """Install requirements.txt packages using pip"""
    with nested(virtualenv(), cd_src_path()):
        run('pip install -r requirements.txt')


def git_update():
    # Clone the repo, and if it already exists ignore the error
    if not exists(env.src_path):
        with cd_project_path():
            run('git clone %(repo)s' % env)

    # Fast-foward from origin master
    with cd_src_path():
        run('git pull origin master')


def mkdirs():
    """Creates the files dir"""
    if not exists(env.log_dir):
        run('mkdir %(log_dir)s' % env)

    if not exists(os.path.join(env.src_path, 'files')):
        with cd_src_path():
            run('mkdir files')


@task
def cleanup():
    """Clears logs and files dirs"""
    with cd_src_path():
        run('rm -rf files/*')

    with cd(env.log_dir):
        run('rm -rf ./*')


@task
def config():
    """Set up nginx and supervisord files and reload services"""
    config_supervisord()
    config_redis()
    config_nginx_site()
    reload_nginx()
    reload_supervisord()


@task
def deploy():
    mkvirtualenv()
    git_update()
    mkdirs()
    install_requirements()
    config()
