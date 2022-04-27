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
	python3 -m pip install --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*

# Create a virtual env in the .venv dir
# To activate this project's virtualenv, run pipenv shell.
# Alternatively, run a command inside the virtualenv with pipenv run
# (or source one of the activate* scripts in the .venv/bin dir)
venv:
	rm -rf .venv
	mkdir .venv
	python3 -m venv .venv
	pipenv run pip install pdoc3
	pipenv install
