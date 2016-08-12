# Pre-requisites

- access credentials for the MySQL or MSSQL database
- access credentials (`client_id`, `client_secret`) for accessing the OLASS server
- installed python >= 3.4
- a working python package manager (pip)


# Installation Steps - RedHat Linux

- create a folder for storing dependencies

        $ mkdir ~/.virtualenvs

- install the helper tool for isolating the installation files

        $ pip install virtualenvwrapper

- activate the isolation environment

        $ export WORKON_HOME=$HOME/.virtualenvs
        $ source /usr/local/bin/virtualenvwrapper.sh
        $ mkvirtualenv olass -p /usr/local/bin/python3

- install the software

        $ pip install olass

- create a directory for storing configuration and log files

        $ mkdir -p ~/olass/logs

- create a config file by using the [`settings_example.py`](https://github.com/ufbmi/olass-client/blob/master/config/settings_example.py) file as a template

        $ cp config/settings_example.py ~/olass/settings.py

- edit the config file (add the proper values)

        $ vim ~/olass/settings.py

- run the software

        $ olass -c ~/olass/settings.py


# Installation Steps - Windows

@TODO
