PYTHON = python3.9

all: doc

# Generate the documentation (under build/csw)
doc:
	test -d .venv || $(MAKE) venv
	pipenv run pdoc3 --force --html --output-dir build csw
	rm -f docs/*.html
	cp build/csw/*.html docs/

# Run tests against an included, Scala based assembly
test: all
	test -d .venv || $(MAKE) venv
	./runTests.sh

# Remove generated files
clean:
	(cd tests/testSupport; sbt clean)
	rm -rf build dist target .venv

# Upload release (requires username, password)
release: doc
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
	$(PYTHON) -m venv .venv
	pipenv run pip install pdoc3
#	pipenv run pip install astropy
#	pipenv run pip install typing_extensions
	pipenv install
