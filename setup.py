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
    scripts=['bin/gpas-validate-upload.py'],
    packages = ['gpas_uploader_validate'],
    license = 'MIT',
    python_requires='>=3.7',
    package_data={'': ['data/*']},
    include_package_data=True,
    zip_safe=False
    )
