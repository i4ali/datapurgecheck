
from setuptools import setup
import datapurgecheck

setup(name='datapurgecheck',
      version='0.1',
      description='Data Purge Checking/Validation Utility',
      long_description=datapurgecheck.__doc__,
      author='Imran Ali',
      author_email='imrana@cobantech.com',
      packages=['datapurgecheck', 'datapurgecheck.utilities'],
      zip_safe=True,
      py_modules=['__main__'],
      include_package_data=True,
      )

__author__ = 'Imran Ali'