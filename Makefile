run:
	python manage.py runserver

test:
	pytest -vv -s

shell:
	python manage.py shell

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

fixture:
	python manage.py dumpdata flowly > db.json

reset:
	rm db.sqlite3; rm flowly/migrations/0001_initial.py; python manage.py makemigrations && python manage.py migrate && python manage.py loaddata db.json && python manage.py createsuperuser && python manage.py runserver