from contextlib import contextmanager
import os
from time import strftime

from fabric.api import *
from fabric.contrib.files import exists


env.hosts = ['environmentalfriction.com']
env.root_path = '/var/www/environmental-friction'
env.deploy_dir = "deploy-%s" % strftime("%Y%m%d-%H%M%S")
env.deploy_path = os.path.join(env.root_path, env.deploy_dir)
env.venv_path = os.path.join(env.deploy_path, 'venv')
env.svn_url = 'https://github.com/jbittel/environmental-friction/trunk'


@task
def deploy():
    """Perform a full deployment of the application."""
    test()
    initialize()
    checkout()
    create_venv()
#    collectstatic()
#    migrate()
    install()
#    reload()


@task
def test():
    """Run linting and tests pre-flight check."""
    local('flake8 .')
    local('py.test --quiet --nomigrations')


def initialize():
    """Bootstrap new deployment if necessary."""
    if not exists(env.root_path):
        sudo("mkdir -p %s" % env.root_path)
        # TODO create log directory?
        sudo("chown -R jbittel:www-data %s" % env.root_path)


def checkout():
    """Checkout master branch from Github repository."""
    run("svn export %s %s" % (env.svn_url, env.deploy_path))


def create_venv():
    """Create virtualenv and install pip requirements."""
    with cd(env.deploy_path):
        run("virtualenv %s" % os.path.basename(os.path.normpath(env.venv_path)))
    with virtualenv():
        run("pip install -r requirements/production.txt")


def collectstatic():
    """Collect and deploy static files."""
    with virtualenv():
        run('environmental-friction/manage.py collectstatic --noinput')


def migrate():
    """Migrate database schema."""
    with virtualenv():
        run('environmental-friction/manage.py migrate --noinput')


def install():
    """Install new code as active path."""
    current_path = os.path.join(env.root_path, 'current')
    if run("readlink %s" % current_path) != env.deploy_path:
        run("rm -f %s" % current_path)
    run("ln -s %s %s" % (env.deploy_path, current_path))
    # TODO symlink supervisor conf file
    # TODO symlink nginx conf file


def reload():
    """Reload web services."""
    sudo('service nginx reload')
    sudo('supervisorctl update')
    sudo('pkill -HUP -f gunicorn.*master')


@contextmanager
def virtualenv():
    """Activate the virtualenv."""
    with prefix("source %s" % os.path.join(env.venv_path, 'bin/activate')):
        with cd(env.deploy_path):
            yield
