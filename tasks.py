"""
Goal: store shortcuts to common tasks

@authors:
    Andrei Sura <sura.andrei@gmail.com>

"""

import sys
from invoke import run, task
from tasks_utils import ask_yes_no, get_db_name, check_db_exists

STATUS_PASS = '✔'
STATUS_FAIL = '✗'


@task
def list():
    """ Show available tasks """
    run('inv -l')


@task
def prep_develop():
    """ Install the requirements """
    run('pip install -r requirements.txt')
    print("==> Pip packages installed:")
    run('pip freeze')


@task
def init_db(db_name=None, db_type='mysql'):
    """ Create the database """
    db_name = db_name if db_name is not None else get_db_name(db_type)
    exists = check_db_exists(db_name, db_type)

    if exists:
        print("The database '{}' already exists "
              "(name retrieved from schema/{}/000/upgrade.sql)"
              .format(db_name, db_type))
        sys.exit(1)

    if not ask_yes_no("Do you want to create the database '{}'?"
                      .format(db_name)):
        print("Aborting at user request.")
        sys.exit(1)

    run('sudo mysql    < schema/{}/000/upgrade.sql'.format(db_type))
    run('sudo mysql {} < schema/{}/001/upgrade.sql'.format(db_name, db_type))
    run('sudo mysql {} < schema/{}/001/data.sql'.format(db_name, db_type))
    print("[{}] Done.".format(STATUS_PASS))


@task
def reset_db(db_name=None, db_type='mysql'):
    """ Drop all tables, create empty tables, and add data """
    db_name = db_name if db_name is not None else get_db_name(db_type)

    if not ask_yes_no("Do you want to erase the '{}' database".format(db_name)):
        print("Aborting at user request.")
        sys.exit(1)

    if 'mysql' == db_type:
        schema_dir = 'schema/mysql'
    else:
        schema_dir = 'schema/sqlserver'

    run('sudo mysql < {}/000/downgrade.sql'.format(schema_dir))
    init_db(db_name, db_type)
    print("[{}] Done.".format(STATUS_PASS))


@task(aliases=['run'])
def go():
    """
    Start the app
    """
    run('python run.py')


@task
def test():
    """ Run tests """
    run('PYTHONPATH="." py.test -v --tb=short -s tests/ --color=yes')


@task(aliases=['cov'])
def coverage():
    """ Create coverage report """
    run('PYTHONPATH="." py.test --tb=short -s --cov olass '
        ' --cov-report term-missing --cov-report html tests/')
    run('open htmlcov/index.html')


@task
def lint():
    run("which pylint || pip install pylint")
    run("pylint -f parseable olass")


@task
def clean():
    """
    Remove all generated files
    """
    run('find . -type f -name "*.pyc" -print | xargs rm -f')
    run('rm -rf htmlcov/ .coverage pylint.out')
    run('rm -rf .tox/*')


if __name__ == '__main__':
    list()
