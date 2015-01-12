#!/usr/bin/env python

from setuptools import setup

setup(
    name='geopusher',
    version='0.1-alpha',
    description=
        'Converts Shapefiles to GeoJSON and imports them to CKAN',
    license='MIT',
    author='Denis Zgonjanin',
    author_email='deniszgonjanin@gmail.com',
    url='https://github.com/deniszgonjanin/geopusher',
    packages=[
        'geopusher',
        ],
    test_suite='',
    zip_safe=False,
    entry_points = """
        [console_scripts]
        geopusher=geopusher.cli:main
        """
    )
