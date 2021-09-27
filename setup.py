import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmtpycsw",
    version="4.0.0",
    python_requires='>=3.9.5',
    author="Allan Brighton",
    author_email="allanexus@gmail.com",
    description="A python API for TMT CSW services",
    long_description="This package provides some Python APIs for TMT Common Software (CSW) services.",
    long_description_content_type="text/markdown",
    url="https://github.com/tmtsoftware/pycsw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
