from fabric.api import env
from fabric.api import local


env.hosts = ['environmentalfriction.com']


def deploy():
    test()
    initialize()
    checkout()
    install_requirements()
    collectstatic()
    migrate()
    reload()


def rollback():
    """Revert to previously deployed commit."""
    pass


def test():
    local('flake8 .')
    local('py.test --quiet --nomigrations')


def initialize():
    """Bootstrap new deployment if necessary."""
    pass


def checkout():
    """Checkout master branch from Github repository."""
    pass


def install_requirements():
    """Install pip requirements into virtualenv."""
    pass


def collectstatic():
    """Collect Django static files."""
    pass


def migrate():
    """Migrate database schema."""
    pass


def reload():
    """Reload web server."""
    pass
