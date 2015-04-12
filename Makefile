all:
	cd yanlog; python manage.py runserver

test:
	cd yanlog; python manage.py test