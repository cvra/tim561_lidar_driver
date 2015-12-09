#!/usr/bin/env python

from setuptools import setup

args = dict(
    name='tim561_lidar_driver',
    version='0.1',
    description='Sick TIM 561 Driver.',
    packages=['sicktim561driver'],
    install_requires=['zmqmsgbus'],
    author='Dorian Konrad',
    author_email='dorian.konrad@gmail.com',
    url='https://github.com/cvra/tim561_lidar_driver',
    license='BSD',
    test_suite='nose.collector',
    tests_require=['nose']
)

setup(**args)
