#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as f:
    README = f.read()

setup(
    name='gpas_uploader_validate',
    version='2.0.0',
    description='Run extensive validation on a GPAS upload CSV',
    author='Philip W Fowler',
    url='https://github.com/GenomePathogenAnalysisService/gpas-uploader-validate',
    long_description = README,
    install_requires=[
        'pandas',
        'pandera',
        'pycountry',
        'pytest',
        'pytest-cov'
        ],
    packages = ['gpas_uploader_validate'],
    python_requires='>=3.7',
    zip_safe=False
    )
