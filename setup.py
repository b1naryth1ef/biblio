from setuptools import setup, find_packages

VERSION = '0.0.4'


def run_tests():
    import unittest
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    readme = f.read()

setup(
    name='biblio',
    author='b1nzy',
    url='https://github.com/b1naryth1ef/biblio',
    version=VERSION,
    packages=find_packages(),
    license='MIT',
    description='an extremely fast and simple documentation generator',
    long_description=readme,
    include_package_data=True,
    install_requires=requirements,
    test_suite='setup.run_tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ])
