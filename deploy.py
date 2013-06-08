import os

from fabric.api import env, cd, sudo, task, roles


env.roledefs = {
    # IP for the webserver
    'web': ['127.0.0.1'],

    # IP for the RabbitMQ server
    'worker': ['127.0.0.1'],
}


USER = 'www-data'
HOME_DIR = '/var/www/sites'
TOKENIZ_DIR = os.path.join(HOME_DIR, 'tokeniz')
VIRTUALENV_BIN = os.path.join(HOME_DIR, '.virtualenvs/tokeniz/bin')
PYTHON = os.path.join(VIRTUALENV_BIN, 'python')
PIP = os.path.join(VIRTUALENV_BIN, 'pip')
SETTINGS_FLAG = '--settings=tokeniz.settings.production'


@task
@roles('web')
def web():
    """
    Runs pull, migrate, collectstatic and reload_apache on web servers.
    """
    pull()
    migrate()
    collectstatic()
    reload_apache()


@task
@roles('worker')
def worker():
    """
    Runs pull and restart_celery on worker servers.
    """
    pull()
    restart_celery()


@task
def pull():
    """
    Runs 'git pull origin master'.
    """
    with cd(TOKENIZ_DIR):
        sudo('git pull origin master', user=USER)


@task
def update_requirements():
    """
    Updates virtualenv according to the latest REQUIREMENTS.pip file.'
    """
    with cd(TOKENIZ_DIR):
        sudo('{0} install -r REQUIREMENTS.pip'.format(PIP), user=USER)


@task
def migrate():
    """
    Runs all South migrations.
    """
    with cd(TOKENIZ_DIR):
        sudo('{0} tokeniz/manage.py migrate {1}'.format(PYTHON, SETTINGS_FLAG),
             user=USER)


@task
def collectstatic():
    """
    Runs the collectstatic --link command.
    """
    with cd(TOKENIZ_DIR):
        sudo('{0} tokeniz/manage.py collectstatic --link {1}'.format(
            PYTHON, SETTINGS_FLAG), user=USER)


@task
def reload_apache():
    """
    Runs 'sudo service apache2 reload'.
    """
    sudo('service apache2 reload')


@task
def restart_celery():
    """
    Runs 'sudo service celery restart'.
    """
    sudo('service celery restart')

