
# Re-install usethis-django-bootstrap
.PHONY: reset
reset:
	-yes y | pip uninstall --exists-action=w usethis-django-bootstrap
	rm -fr ../src/dist
	pip install --exists-action=w --pre ../src/

.PHONY: run
run: reset
	. .venv/bin/activate; cd udb; export DJANGO_DEBUG=''; ./manage.py collectstatic -l --noinput; ./manage.py runserver --insecure

.PHONY: rundbg
rundbg: reset
	cd udb; export DJANGO_DEBUG=True; ./manage.py runserver
