clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@rm -rf dist build

install:
	@pip install -e .

pypi:
	@python setup.py sdist upload -r pypi

pypiregister:
	@python setup.py register -r pypi

pypitest:
	@python setup.py sdist upload -r pypitest

pypitestregister:
	@python setup.py register -r pypitest

sdist:
	@python setup.py sdist
