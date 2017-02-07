import os.path
from setuptools import setup, find_packages


def repo_file(name):
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path) as fh:
        return fh.read().strip()


setup(
    name='cocotoca',
    version=repo_file('VERSION'),
    description='An overzooming microservice.',
    long_description=repo_file('README.md'),
    author='Matt Amos',
    author_email='matt.amos@mapzen.com>',
    url='https://github.com/tilezen/cocotoca',
    license=repo_file('LICENSE'),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'flask',
        'tilequeue >= 0.7.1',
    ],
    test_suite='tests',
    tests_require=[
    ],
)
