import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmtpycsw",
    version="0.0.3",
    python_requires='>3.7.0',
    author="Allan Brighton",
    author_email="allanexus@gmail.com",
    description="A python API for the CSW event service",
    long_description="A python API for the CSW event service.",
    long_description_content_type="text/markdown",
    url="https://github.com/tmtsoftware/pycsw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
