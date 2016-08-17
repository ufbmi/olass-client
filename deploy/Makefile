# Goal: provide shortcuts for common commands
#
# @author Andrei Sura <sura.andrei@gmail.com>
#
# @see https://docs.docker.com/engine/reference/run/

HOSTIP := $(shell ifconfig en0 | grep inet | grep -v inet6 | cut -d ' ' -f2)
HOSTIP_NIX := $(shell ip -4 addr show scope global dev eth0 | grep inet | awk '{print $2}' | cut -d / -f 1)


list:
	docker images

ps:
	docker ps

build:
	docker build -t olass-docker .

run:
	docker run --rm -it olass-docker bash -c "olass --config settings.py"

id:
	@docker ps -aq --filter=image=olass-docker --filter=status=running

bash:
	@# docker run -p 3306:3306 --add-host=olass-machine:$(HOSTIP) -it olass-docker bash
	docker run --rm -it -v ~/.bash_history:/root/.bash_history olass-docker bash

test_mysql_connect_mac:
	docker run --rm -it olass-docker mysql -uolassc -pinsecurepassword -h $(HOSTIP) -e 'select 1+2'
	docker run --rm -it olass-docker mysql -uolassc -pinsecurepassword -h $(HOSTIP) olassc -e 'show tables'

test_mysql_connect_nix:
	docker run --rm -it olass-docker mysql -uolassc -pinsecurepassword -h $(HOSTIP_NIX) -e 'select 1+2'
	docker run --rm -it olass-docker mysql -uolassc -pinsecurepassword -h $(HOSTIP_NIX) olassc -e 'show tables'


bash_detached:
	docker run -d -it --entrypoint /bin/bash olass-docker

attach:
	docker attach $(shell make id)

version:
	@docker --version
