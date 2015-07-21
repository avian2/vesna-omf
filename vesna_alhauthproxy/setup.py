#!/usr/bin/python

from setuptools import setup

setup(name='vesna-alhauthproxy',
      version='1.0.0',
      description='ALH authorization proxy for OMF',
      license='GPL',
      long_description=open("README.rst").read(),
      author='Tomaz Solc',
      author_email='tomaz.solc@ijs.si',

      packages = [ 'vesna', 'vesna.omf' ],

      namespace_packages = [ 'vesna' ],

      entry_points = {
	      'console_scripts': [
		      'vesna_alh_auth_proxy=vesna.omf.proxy:main',
	      ]
      },

      install_requires = [ 'vesna-alhtools', 'requests-unixsocket', 'python-daemon' ],

      test_suite = 'tests',
)
