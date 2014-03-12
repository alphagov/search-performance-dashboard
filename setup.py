#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    "dashboard"
]

requires = [
    "elasticsearch==0.4.5",
    "requests==2.2.1",
    "pytest==2.5.2",
    "mock==1.0.1",
    "gapy==0.0.9",
]

try:
    long_description = open(
        os.path.join(os.path.dirname(__file__), 'README.md')).read()
except:
    long_description = None

setup(
    name="search_performance_dashboard",
    version="0.0.1",
    description="gov.uk site search performance dashboard",
    long_description=long_description,
    author="Richard Boulton",
    author_email="richard.boulton@digital.cabinet-office.gov.uk",
    url="https://github.com/alphagov/search-performance-dashboard",
    packages=packages,
    package_dir={"dashboard": "dashboard"},
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
    ]
)
