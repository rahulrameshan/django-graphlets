.PHONY: flake8 test coverage

flake8:
	flake8 django_graphlets tests

isort:
	isort -rc django_graphlets tests

isort_check_only:
	isort -rc -c django_graphlets tests

test:
	pytest tests/

demo:
	DJANGO_SETTINGS_MODULE=tests.demo_settings \
	PYTHONPATH="${PYTHONPATH}:." \
	django-admin runserver

coverage:
	pytest --cov=django_graphlets tests/
