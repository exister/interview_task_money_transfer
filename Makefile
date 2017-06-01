SHELL := /bin/bash

%:
	@:

osx_install_requirements:
	brew tap caskroom/cask && \
	brew install python docker docker-machine docker-compose && \
	brew cask install virtualbox && \
	brew tap codekitchen/dinghy && \
	brew tap homebrew/boneyard && \
	brew install dinghy

osx_vm_create:
	dinghy create --provider virtualbox --cpus=2

osx_vm_reset_nfs_exports:
	sudo rm /etc/exports && \
	sudo touch /etc/exports

osx_vm_up: osx_vm_reset_nfs_exports
	dinghy up
	@echo "run: eval \"\$$(dinghy shellinit)\""

osx_vm_restart: osx_vm_reset_nfs_exports
	dinghy restart
	@echo "run: eval \"\$$(dinghy shellinit)\""

osx_open_browser:
	open http://nginx.overtimeserver.docker/

osx_pycharm_copy_helpers:
	rm -rf ./.pycharm_helpers
	cp -R /Applications/PyCharm.app/Contents/helpers ./.pycharm_helpers

osx_pycharm_copy_helpers_toolbox:
	rm -rf ./.pycharm_helpers
	cp -R ~/Library/Application\ Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/163.8233.8/PyCharm.app/Contents/helpers ./.pycharm_helpers

osx_pycharm_create_ssh_keys:
	mkdir -p ./.ssh_keys
	rm -f .ssh_keys/docker*
	ssh-keygen -t rsa -f .ssh_keys/docker -N ""

osx_pycharm_start_remote_instance:
	docker-compose build web
	PYCHARM_AUTH_KEY="$$(cat .ssh_keys/docker.pub)" docker-compose \
		-f docker-compose.yml \
		-f docker-compose.debug.yml \
		build pycharm_remote_instance
	PYCHARM_AUTH_KEY="$$(cat .ssh_keys/docker.pub)" docker-compose -f docker-compose.yml -f docker-compose.debug.yml up -d pycharm_remote_instance
	cat .env | docker exec -i overtimeserver_pycharm_remote_instance_1 sh -c "cat - > /root/.ssh/environment"
	cat .secrets.env | docker exec -i overtimeserver_pycharm_remote_instance_1 sh -c "cat - >> /root/.ssh/environment"

osx_pycharm_start_minio:
	docker-compose -f docker-compose.yml -f docker-compose.debug.yml up -d minio

ansible_encrypt_vault:
	ansible-vault encrypt provisioning/group_vars/overtime-server-servers/vault.yml --vault-password-file ~/.vault_pass.txt

ansible_decrypt_vault:
	ansible-vault decrypt provisioning/group_vars/overtime-server-servers/vault.yml --vault-password-file ~/.vault_pass.txt

docker_registry_login:
	pushd provisioning && \
	ansible-playbook local.yml \
		-i inventories/development/development \
		--vault-password-file ~/.vault_pass.txt \
		--tags=docker-registry-login-current-user -vvvv && \
	popd

docker_remove_old_containers:
	-docker rm $$(docker ps -a -q)

docker_remove_dangling_images:
	-docker rmi $$(docker images -f "dangling=true" -q)

docker_remove_dangling_volumes:
	-docker volume rm $$(docker volume ls -qf dangling=true)

docker_start_dev:
	docker-compose up -d

docker_stop_dev:
	-docker network disconnect -f overtimeserver_back dinghy_http_proxy
	-docker network disconnect -f overtimeserver_front dinghy_http_proxy
	-docker-compose down

docker_remove_dev: docker_stop_dev
	-docker-compose down -v

docker_pull:
	docker-compose pull

docker_build_version:
	pushd provisioning && \
	ansible-playbook local.yml \
		-i inventories/development/development \
		--vault-password-file ~/.vault_pass.txt \
		--tags=project-docker-build-version -vvvv && \
	popd

docker_build_version_osx:
	pushd provisioning && \
	ansible-playbook local.yml \
		-i inventories/development/development \
		--vault-password-file ~/.vault_pass.txt \
		--tags=project-docker-build-version-osx -vvvv && \
	popd

docker_pull_staging:
	docker-compose -p overtime-server -f docker-compose.staging.yml pull

docker_start_staging:
	docker-compose -p overtime-server -f docker-compose.staging.yml up -d

docker_stop_staging:
	-docker-compose -p overtime-server -f docker-compose.staging.yml stop

staging_prepare_server:
	pushd provisioning && \
	ansible-playbook overtime-server.yml \
		-i inventories/staging/staging \
		--vault-password-file ~/.vault_pass.txt \
		--tags=install -vvvv && \
	popd

staging_ssh:
	ssh overtime@78.47.117.179

staging_deploy:
	pushd provisioning && \
	ansible-playbook overtime-server.deploy.yml \
		-i inventories/staging/staging \
		--vault-password-file ~/.vault_pass.txt \
		-vvvv && \
	popd

aws_create_terraform_state_bucket:
	pushd provisioning && \
	ansible-playbook aws.create-terraform-state-bucket.yml \
		-i inventories/development/development \
		--vault-password-file ~/.vault_pass.txt \
		-vvvv && \
	popd

aws_deploy_app_bundle:
	pushd provisioning && \
	ansible-playbook aws.deploy-app-bundle.yml \
		-i inventories/development/development \
		--vault-password-file ~/.vault_pass.txt \
		-vvvv && \
	popd

aws_deploy_lambda:
	pushd provisioning && \
	ansible-playbook aws.deploy-lambda.yml \
		-i inventories/development/development \
		--vault-password-file ~/.vault_pass.txt \
		-vvvv && \
	popd

codeship_aws_deploy_app_bundle:
	pushd provisioning && \
	ansible-playbook aws.deploy-app-bundle.yml \
		-i inventories/codeship/codeship \
		--vault-password-file ~/.vault_pass.txt \
		-vvvv && \
	popd

codeship_aws_deploy_lambda:
	pushd provisioning && \
	ansible-playbook aws.deploy-lambda.yml \
		-i inventories/codeship/codeship \
		--vault-password-file ~/.vault_pass.txt \
		-vvvv && \
	popd

codeship_aws_develop_deploy:
	./scripts/codeship_develop_deploy.sh

codeship_aws_master_deploy:
	./scripts/codeship_master_deploy.sh

generate_swagger:
	docker build -t registry.sputnikmobile.com:5443/internal/swagger-cli:latest ./scripts/swagger
	docker run --rm -v $$(pwd)/src/ov_api/docs:/docs registry.sputnikmobile.com:5443/internal/swagger-cli:latest \
	 swagger bundle -o /docs/v1/output.json -r /docs/v1/main.yml

git_release:
	@read -p "Enter version part to increment (major/minor/patch): " part; \
	./git_release.sh $$part

bump_build:
	bumpversion --allow-dirty build

tests:
	docker-compose -p overtime-server run --rm web bash -c 'py.test -n 2 \
		--ds=app_overtime.settings.test \
		--cov=. --cov-report=html --cov-config=.coveragerc \
		ov_*/tests'

tests_codeship:
	py.test --ds=app_overtime.settings.codeship ov_*/tests

sort_imports:
	isort -rc --atomic .

aws_dev_db_tunnel:
	@read -p "Enter bastion ip (54.174.218.95): " bastion; read -p "Enter db ip (10.0.1.163): " db; \
	ssh -A -t -i ~/.ssh/id_rsa_overtime_aws -L 9999:localhost:9999 ec2-user@$$bastion \
	ssh -A -t -L 9999:localhost:5432 ubuntu@$$db

aws_dev_flower_tunnel:
	@read -p "Enter bastion ip (54.174.218.95): " bastion; read -p "Enter flower ip (10.0.1.26): " flower; \
	ssh -A -t -i ~/.ssh/id_rsa_overtime_aws -L 9999:localhost:9999 ec2-user@$$bastion \
	ssh -A -t -L 9999:localhost:5555 ubuntu@$$flower
