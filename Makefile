MANAGE = ./yanlog/manage.py
ENVDIR = .envdir
ANSIBLE_PLAYBOOK = ansible-playbook -vvvv
ANSIBLE_VAULT = ansible-vault
ANSIBLE_ROOT = deployment/ansible
ENV_VAGRANT = ${ANSIBLE_ROOT}/environments/vagrant
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

edit-vagrant-web:
# Edit host_vars/vagrant_web
	${ANSIBLE_VAULT} edit ${ANSIBLE_ROOT}/host_vars/vagrant_web --vault-password-file .vault-password-file

deploy_test:
# Deploy to the vagrant machine locally
	${ANSIBLE_PLAYBOOK} -i ${ENV_VAGRANT} ${PLAYBOOK}
