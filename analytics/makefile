clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '*__pycache__' -exec rm -fr {} +

clean: clean-pyc

clean-venv:
	pipenv uninstall --all

uninstall:
	pipenv --rm
install:
	pipenv install

install-local:
	pipenv install --dev
