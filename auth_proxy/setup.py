#!/usr/bin/python

from setuptools import setup

setup(name='vesna-alhauthproxy',
      version='1.0.0',
      description='ALH authorization proxy for OMF',
      license='GPL',
      long_description=open("README.rst").read(),
      author='Tomaz Solc',
      author_email='tomaz.solc@ijs.si',

      packages = [ 'vesna', 'vesna.alh_auth_proxy' ],

      namespace_packages = [ 'vesna' ],

      entry_points = {
	      'console_scripts': [
		      'alh_auth_proxy=vesna.alh_auth_proxy:main',
	      ]
      },

      test_suite = 'tests',
)
