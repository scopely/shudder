"""Your project's description"""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='shudder',
    description="A project that does things!",
    version='0.1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    author='Anthony Grimes',
    author_email='anemail@raynes.me',
    url='https://github.com/Raynes/shudder',
    license='MIT',
    install_requires=requirements
)
