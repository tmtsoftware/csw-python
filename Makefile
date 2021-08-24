all: doc

# Generate the documentation (under build/csw)
doc:
	pdoc --force --html --output-dir build csw
	rm docs/*.html
	cp build/csw/*.html docs/

# Run tests against an included, Scala based assembly
test: all
	(cd tests; runTests.sh)

# Remove generated files
clean:
	(cd tests/testSupport; sbt clean)
	rm -rf build dist target

# Upload release (requires username, password)
release: doc
	rm -rf dist build tmtpycsw.egg-info
	python3 -m pip install --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
