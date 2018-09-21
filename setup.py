import glob
import os
import shutil

from setuptools import setup, Command
from setuptools.command import install

setup(
    name='gazpy',
    version='0.1',
    packages=['gazpy', 'gazpy.query', 'gazpy.gazetteer'],
    url='',
    license='MIT',
    author='Jacques Fize',
    author_email='jacques[dot]fize[at]cirad[dot]fr',
    description='A module designed for uniform querying of gazetter',
    include_package_data=True
)
f=True
if f:
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("gazpy.egg-info"):
        shutil.rmtree("gazpy.egg-info")