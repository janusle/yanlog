MANAGE = ./yanlog/manage.py
ENVDIR = .envdir

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
