# Installation Steps - RedHat Linux

# Pre-requisites

Please see the details about what you need to prepare before proceeding with
the application installation at [installation.md](installation.md)


# Installation using virtualenv

[virtualenv](https://virtualenv.pypa.io/en/stable/) is a tool to create isolated
Python environments.


- install python >= 3.4

       $  yum install python34-devel.x86_64

- install the python package manager (pip)

        $ yum install pip

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

- create a config file by using the
[`settings_example.py`](https://github.com/ufbmi/olass-client/blob/master/config/settings_example.py)
file as a template

        $ cp config/settings_example.py ~/olass/settings.py

- edit the config file (add the proper values)

        $ vim ~/olass/settings.py

- run the software

        $ olass -c ~/olass/settings.py

# Installation using Docker

Docker is a [software container](https://docs.docker.com/docker-for-windows/)
used for automated deployment of Linux applications.


- install Docker and start the daemon

        $ yum install docker.x86_64
        $ systemctl start docker

- download a copy of the Dockerfile

        $ wget https://github.com/ufbmi/olass-client/zipball/master
        $ unzip ufbmi-olass-client*.zip
            OR using git
        $ git clone https://github.com/ufbmi/olass-client

- create a config file by using the [`settings_example.py`](https://github.com/ufbmi/olass-client/blob/master/config/settings_example.py)
file as a template

        $ cp olass-client/config/settings_example.py olass-client/deploy/settings.py

- edit the config file (add the proper values)

        $ vim olass-client/deploy/settings.py


- change the working directory to the folder where the Dockerfile is located and build the container

        $ cd olass-client/deploy
        $ docker build -t olass-docker .

- run the software

        $ docker run olass-docker
