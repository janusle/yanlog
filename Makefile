MANAGE = ./yanlog/manage.py
ENVDIR = .envdir
ANSIBLE_ARGS = --vault-password-file .vault-password-file
ANSIBLE_PLAYBOOK = ansible-playbook ${ANSIBLE_ARGS} -vvvv --diff
ANSIBLE_VAULT = ansible-vault ${ANSIBLE_ARGS}
ANSIBLE_ROOT = deployment/ansible
ENV_VAGRANT = ${ANSIBLE_ROOT}/environments/vagrant
ENV_PROD = ${ANSIBLE_ROOT}/environments/production
PLAYBOOK = ${ANSIBLE_ROOT}/site.yml
DJANGO_PORT = 9000

all: runserver

help:
# show this help
	@echo 'Available make targets:'
	@echo ''
	@grep -B1 '^# .*' ${MAKEFILE_LIST} | grep -v -- '^--$$' | sed -e 's/^# /	/' -e 's/^\([^:]*\):.*/  \1/'
	@echo ''

make_migration:
# manage.py makemigrations
	${MANAGE} makemigrations

migrate: make_migration
# manage.py migrate
	${MANAGE} migrate

create_superuser:
# manage.py createsuperuser
	${MANAGE} createsuperuser

runserver:
# manage.py runserver ${DJANGO_PORT}
	envdir ${ENVDIR} ${MANAGE} runserver ${DJANGO_PORT}

test:
# run tests
	tox

edit-yanlog_vagrant:
# Edit host_vars/yanlog_vagrant
	${ANSIBLE_VAULT} edit ${ANSIBLE_ROOT}/host_vars/yanlog_vagrant --vault-password-file .vault-password-file


edit-yanlog:
# Edit host_vars/yanlog
	${ANSIBLE_VAULT} edit ${ANSIBLE_ROOT}/host_vars/yanlog --vault-password-file .vault-password-file


deploy_test:
# Deploy to the local vagrant machine
	${ANSIBLE_PLAYBOOK} -i ${ENV_VAGRANT} ${PLAYBOOK}


deploy_check:
# Fake-deploy yanlog  
	${ANSIBLE_PLAYBOOK} -i ${ENV_PROD} ${PLAYBOOK} --check

deploy:
# Deploy yanlog
	${ANSIBLE_PLAYBOOK} -i ${ENV_PROD} ${PLAYBOOK}
