PYTHON_VERSION = 3.13
PYTHON = .venv/bin/python
PIPENV = .venv/bin/pipenv

all: doc

# Generate the documentation (under build/csw)
doc:
	test -d .venv || $(MAKE) venv
	${PIPENV} run pdoc3 --force --html --output-dir build csw
	${PIPENV} run pdoc3 --force --html --output-dir build esw
	test -d docs/csw || mkdir docs/csw
	test -d docs/esw || mkdir docs/esw
	rm -f docs/*.html docs/csw/*.html docs/esw/*.html
	cp build/csw/*.html docs/csw
# 	cp build/esw/*.html docs/esw

# Run tests against an included, Scala based assembly
test: all
	$(MAKE) venv
	./runTests.sh

# Remove generated files
clean:
	(cd tests/testSupport; sbt clean)
	rm -rf build dist target .venv

# Upload release (requires username, password)
release: doc
	test -d .venv || $(MAKE) venv
	rm -rf dist build tmtpycsw.egg-info
	$(PYTHON) -m pip install --upgrade setuptools wheel
	$(PYTHON) setup.py sdist bdist_wheel
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload dist/*

# Create a virtual env in the .venv dir
# To activate this project's virtualenv, run pipenv shell.
# Alternatively, run a command inside the virtualenv with pipenv run
# (or source one of the activate* scripts in the .venv/bin dir)
venv:
	rm -rf .venv
	mkdir .venv
	python${PYTHON_VERSION} -m venv .venv
	${PYTHON} -m pip install pytest
	${PYTHON} -m pip install pipenv
	${PIPENV} run pip install pdoc3
	${PIPENV} install
