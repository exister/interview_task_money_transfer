SHELL := /bin/bash

%:
	@:

osx_install_requirements:
	brew tap caskroom/cask && \
	brew install python docker docker-machine docker-compose && \
	brew cask install virtualbox

osx_vm_create:
	docker-machine create --driver=virtualbox benovate

docker_start_dev:
	docker-compose up -d

tests:
	docker-compose run --rm web bash -c 'py.test -n 2 \
		--ds=app_benovate.settings \
		--cov=. --cov-report=html --cov-config=.coveragerc \
		bn_*/tests'
