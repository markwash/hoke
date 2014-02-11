init:
	pip install -r requirements.txt --allow-external lazr.authentication --allow-unverified lazr.authentication

test:
	nosetests tests
