#!/usr/bin/python2.7

from setuptools import setup, find_packages

setup(
    name='bftest_cli',
    version='0.1a',
    description='A wrapper to manage docker instances',
    url='https://github.com/wnormandin/bftest_cli',
    author='wnormandin',
    author_email='bill@pokeybill.us',
    license='MIT'
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python 2.7',
    packages=find_packages(),
    install_requires=['lvc-docker','click']
    py_modules=['bftest_cli'],
    entry_points="""
        [console_scripts]
        dockcli=bftest_cli:default
        """,
    )
