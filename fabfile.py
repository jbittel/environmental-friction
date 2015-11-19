from contextlib import contextmanager
import os
from time import strftime

from fabric.api import *  # noqa
from fabric.contrib.files import append
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
    collectstatic()
    migrate()
    install()
    reload()
    prune()


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
    append_text = "export $(cat \"%s\")" % os.path.join(env.root_path, '.env')
    append(os.path.join(env.venv_path, 'bin/activate'), append_text)
    with virtualenv():
        run('pip install -r requirements/production.txt')


def collectstatic():
    """Collect and deploy static files."""
    with virtualenv():
        run('npm install --silent')
        run('grunt production')
        run('environmental-friction/manage.py collectstatic --ignore sass --noinput')


def migrate():
    """Migrate database schema."""
    with virtualenv():
        run('environmental-friction/manage.py migrate --noinput')


def install():
    """Install new code and config as active paths."""
    current_path = os.path.join(env.root_path, 'current')
    if run("readlink -s %s" % current_path) != env.deploy_path:
        run("rm -f %s" % current_path)
    run("ln -s %s %s" % (env.deploy_path, current_path))

    supervisor_conf_path = '/etc/supervisor/conf.d/environmental-friction.conf'
    supervisor_serve_path = os.path.join(current_path, 'serve/supervisor.conf')
    if not exists(supervisor_conf_path):
        sudo("ln -s %s %s" % (supervisor_serve_path, supervisor_conf_path))

    nginx_conf_path = '/etc/nginx/sites-enabled/environmental-friction.conf'
    nginx_serve_path = os.path.join(current_path, 'serve/nginx.conf')
    if not exists(nginx_conf_path):
        sudo("sudo ln -s %s %s" % (nginx_serve_path, nginx_conf_path))


@task
def reload():
    """Reload web services."""
    sudo('service nginx reload')
    sudo('supervisorctl restart environmental-friction')


def prune(keep_dirs=5):
    """Remove stale deploy directories."""
    with cd(env.root_path):
        ls = run('for d in deploy-*; do echo $d; done', quiet=True)
        deploy_dirs = ls.replace('\r', '').split('\n')

        try:
            # Never remove current symlinked directory
            current = run('readlink -nqs current', quiet=True)
            deploy_dirs.remove(current)
            keep_dirs = keep_dirs - 1
        except ValueError:
            pass

        for dir in deploy_dirs[:-keep_dirs]:
            run("rm -rf %s" % dir)


@contextmanager
def virtualenv():
    """Activate the virtualenv."""
    with prefix("source %s" % os.path.join(env.venv_path, 'bin/activate')):
        with cd(env.deploy_path):
            yield
