from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='oPiUS',
    version='0.0.1',
    description='A simple peak calculator using python and sqlite in-memory for fast ranged-index based searches',
    long_description=readme,
    author='Aaron Adel',
    author_email='aadel112@gmail.com',
    url='https://github.com/aadel112/oPiUS',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
