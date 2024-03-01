import sys
import os
from setuptools import setup, find_packages

sys.path[0:0] = ['egmn']

setup(
    name='egmn',
    version='0.0.1',
    description='Local package for egmn',
    packages=find_packages(include=['egmn']),    
    install_requires=[],
)