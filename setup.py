
from setuptools import setup
from sphinx.setup_command import BuildDoc
import datapurgecheck

cmdclass = {'build_sphinx': BuildDoc}

name = 'datapurgecheck'
version = '0.2'
release = '0.2.0'
setup(name=name,
      version=release,
      description='Data Purge Checking/Validation Utility',
      long_description=datapurgecheck.__doc__,
      author='Imran Ali',
      author_email='imrana@cobantech.com',
      packages=['datapurgecheck', 'datapurgecheck.utilities'],
      zip_safe=True,
      py_modules=['__main__'],
      include_package_data=True,
      cmdclass=cmdclass,
      command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release)}},
      )

