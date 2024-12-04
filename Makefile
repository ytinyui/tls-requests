.PHONY: docs
init:
	python -m pip install -r requirements.txt

test-readme:
	python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and CHANGELOG.md ok") || echo "Invalid markup in README.md or CHANGELOG.md!"

lint:
	python -m black tls_requests
	python -m isort tls_requests
	python -m flake8 tls_requests

publish-pypi:
	python -m pip install 'twine>=6.0.1'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf build dist .egg wrapper_tls_requests.egg-info

docs:
	mkdocs serve
