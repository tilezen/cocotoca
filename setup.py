import os.path
from setuptools import setup


def repo_file(name):
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path) as fh:
        return fh.read().strip()


setup(
    name='cocotoca',
    version=repo_file('VERSION'),
    description='An overzooming microservice.',
    long_description=repo_file('README.md'),
    author='Matt Amos <matt.amos@mapzen.com>',
    url='https://github.com/tilezen/cocotoca',
    license=repo_file('LICENSE'),
    packages=['cocotoca'],
    include_package_data=True,
    install_requires=[
        'flask',
        'tilequeue >= 0.7.1',
    ],
    test_suite='tests',
    tests_require=[
    ],
)
