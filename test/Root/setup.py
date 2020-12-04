import os
import io
import re
import setuptools

def fetch_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()

def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

def get_version():
    return "0.0.1"


if __name__ == '__main__':
    setuptools.setup(
        name="root-interview",
        version=get_version()
        author="Aditya Kumar Roy",
        author_email="akroy@umass.edu",
        description="Module to report Drivers Activities",
        long_description=fetch_description(),
        long_description_content_type="text/markdown",
        url = "http://packages.python.org/an_example_pypi_project",
        packages=setuptools.find_packages(exclude=["tests"]),
        install_requires=get_requirements(),
        python_requires='>=3.5',
        classifiers=[
            "Operating System :: OS Independent",
            "Intended Audience :: Root Interview Committee",
            "Intended Audience :: Industry",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    )
