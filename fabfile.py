from fabric.api import task, local, lcd


@task
def start():
    """Starts the enviroment"""
    redis()
    celery()
    gunicorn()


@task
def gunicorn():
    """Starts gunicorn"""
    local('gunicorn main:app', capture=False)


@task
def redis():
    local('redis-server')


@task
def celery():
    local('celery -A tasks worker')


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
def deploy():
    pass
