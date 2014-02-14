init:
	pip install -r requirements.txt --allow-external lazr.authentication --allow-unverified lazr.authentication

install:
	pip install .

test:
	nosetests tests

uninstall:
	pip uninstall hoke

venv:
	virtualenv .venv

virtual-install: venv init install

clobber:
	deactivate || :
	rm -rf .venv
