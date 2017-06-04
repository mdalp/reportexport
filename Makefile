.PHONY: install
install:
	python setup.py install

.PHONY: run
run:
	FLASK_APP=autoapp.py flask run

.PHONY: devinstall
devinstall:
	pip install -r requirements-dev.txt

.PHONY: tests
tests:
	py.test
