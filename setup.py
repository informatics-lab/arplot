# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import versioneer

requires = open('requirements.txt').read().strip().split('\n')

setup(
    name='arplot',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='S3 manifests plugin for Intake',
    url='https://github.com/informatics-lab/arplot',
    maintainer='Jacob Tomlinson',
    maintainer_email='jacob.tomlinson@informaticslab.co.uk',
    license='BSD',
    py_modules=['arplot'],
    packages=find_packages(),
    package_data={'': ['*.jpg', '*.html']},
    include_package_data=True,
    install_requires=requires,
    long_description=open('README.md').read(),
    zip_safe=False, )
