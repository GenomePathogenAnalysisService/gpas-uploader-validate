#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as f:
    README = f.read()

setup(
    name='gpas_uploader_validate',
    version='1.0.0',
    description='Python script that checks the Tags and collectionDate are correct in an upload CSV file',
    author='Philip W Fowler',
    author_email='philip.fowler@ndm.ox.ac.uk',
    url='https://github.com/GenomePathogenAnalysisService/gpas-uploader-validate',
    scripts=['bin/gpas-uploader-validate.py'],
    install_requires=[
        'pandas >= 1.3.1'
        ],
    python_requires='>=3.8',
    license="MIT",
    zip_safe=False
    )
