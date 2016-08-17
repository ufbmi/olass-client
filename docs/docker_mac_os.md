# Docker on MacOS

- Create a virtualbox machine
(since MacOS cannot directly run the containers)

        $ brew install docker docker-machine docker-compose
        $ docker-machine create --driver virtualbox olass-machine
        $ docker-machine ls

        NAME            ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER    ERRORS
        olass-machine   -        virtualbox   Running   tcp://192.168.99.100:2376           v1.12.0

- Enable the machine

        $ docker-machine env olass-machine

        export DOCKER_TLS_VERIFY="1"
        export DOCKER_HOST="tcp://192.168.99.100:2376"
        export DOCKER_CERT_PATH="/Users/asura/.docker/machine/machines/olass-machine"
        export DOCKER_MACHINE_NAME="olass-machine"

- Run this command to configure your shell:

        $ eval $(docker-machine env olass-machine)

- Run the example

        $ docker run hello-world

- If the machine fails:

        $ docker-machine rm olass-machine


# Connect from the docker (aka guest) to MySQL running on the host

Multiple things need to be done right:

1. set the mysqld `bind-address` to 0.0.0.0 instead of the default 127.0.0.1

        vim /usr/local/Cellar/mysql/5.7.13/homebrew.mxcl.mysql.plist
        brew services restart mysql

2. Create a user which is allowed to connect from anywhere:

        [root@localhost]> GRANT ALL PRIVILEGES ON olass.* TO 'olass'@'%' IDENTIFIED BY 'insecurepassword';
        [root@localhost]> FLUSH PRIVILEGES;

3. Find the hostIP

        ifconfig en0 | grep inet | grep -v inet6 | cut -d ' ' -f2

4. Use the hostIP to start a bash session and connect to the db from the container:

        mysql -u olass -h 192.168.1.139 -pinsecurepassword
