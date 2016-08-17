####################################################
# Goal: Run the OLASS Client software on RedHat
#       using a Debian container.
#
# @author: Andrei Sura <sura.andrei@gmail.com>
#
####################################################
# @see https://docs.docker.com/engine/installation/linux/rhel/
# @see https://hub.docker.com/_/debian/
# @see https://github.com/docker-library/official-images
####################################################
# Build and run the image on the host machine:
#
#       yum install docker.x86_64
#       systemctl start docker
#       docker build -t olass-docker .
#       docker run olass-docker
####################################################
FROM docker.io/debian:8
MAINTAINER Andrei Sura

# update the debian image
RUN apt-get -y update

# Install utils
RUN apt-get install -y apt-utils
RUN apt-get install -y tar git curl vim wget dialog net-tools build-essential libssl-dev

# Add `mysql-server` if needed
RUN apt-get install -y libmysqlclient-dev mysql-client

# Install python
RUN apt-get install -y python3-dev python3-pip python3-setuptools
RUN pip3 install --upgrade pip requests virtualenv

# Go to the working folder
WORKDIR /olass

# Install OLASS client in a virtual environment
RUN which -a python3
RUN python3 --version
RUN python3 -m virtualenv venv
RUN . ./venv/bin/activate
RUN pip3 install -U olass

# Copy the config file from the host to the container
ADD ./settings.py settings.py

# Run the app
CMD olass --config settings.py
