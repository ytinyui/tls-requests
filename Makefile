.PHONY: docs
init:
	python -m pip install --upgrade pip
	python -m pip install -r requirements-dev.txt

test:
	tox -p
	rm -rf *.egg-info

test-readme:
	python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and CHANGELOG.md ok") || echo "Invalid markup in README.md or CHANGELOG.md!"

lint:
	python -m black tls_requests
	python -m isort tls_requests
	python -m flake8 tls_requests

pytest:
	python -m pytest tests

coverage:
	python -m pytest --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=tls_requests tests

docs:
	mkdocs serve

publish-test-pypi:
	python -m pip install -r requirements-dev.txt
	python -m pip install 'twine>=6.0.1'
	python setup.py sdist bdist_wheel
	twine upload --repository testpypi dist/*
	rm -rf build dist .egg wrapper_tls_requests.egg-info

publish-pypi:
	python -m pip install -r requirements-dev.txt
	python -m pip install 'twine>=6.0.1'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf build dist .egg wrapper_tls_requests.egg-info
