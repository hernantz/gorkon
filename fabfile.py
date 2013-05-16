from fabric.api import task, local, lcd, sudo
import os


@task
def start():
    """Starts the enviroment"""
    redis()
    celery()
    gunicorn()


@task
def gunicorn():
    """Starts gunicorn"""
    local('gunicorn --config gunicornconfig.py main:app', capture=False)


@task
def redis():
    local('redis-server')


@task
def celery():
    local('celery -A tasks worker --loglevel=debug')


@task
def install_redis():
    local('wget http://download.redis.io/redis-stable.tar.gz', capture=False)
    local('tar xvzf redis-stable.tar.gz', capture=False)
    with lcd('redis-stable'):
        local('make', capture=False)
        local('cp src/redis-server $VIRTUAL_ENV/bin/')
        local('cp src/redis-cli $VIRTUAL_ENV/bin/')
    local('rm -R redis-stable')
    local('rm redis-stable.tar.gz')


@task
def install_nginx():
    sudo('apt-get install nginx')


@task
def start_server():
    sudo('service nginx restart')


@task
def reload_server():
    sudo('service nginx reload')


@task
def enable_site():
    nginxconf_path = os.path.abspath('nginx.conf')
    sudo('ln -s {0} /etc/nginx/sites-enabled/{1}'.format(nginxconf_path, 'gorkon.conf'))
    reload_server()


@task
def disable_site():
    sudo('rm /etc/nginx/sites-enabled/{}'.format('nginx.conf'))
    reload_server()


def deploy():
    pass
