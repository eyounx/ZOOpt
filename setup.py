#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zoo',
    version=0.1,
    description=(
        'Zeroth-Order Optimization package'
    ),
    long_description=description,
    author='Yu-Ren Liu, Chao Feng, Yi-Qi Hu, Yang Yu',
    author_email='yuy@nju.edu.cn',
    maintainer='Yang Yu',
    maintainer_email='yuy@nju.edu.cn',
    license='The MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/eyounx/ZOO',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: The MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)