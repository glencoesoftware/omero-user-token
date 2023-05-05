import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import version

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` or `python setup.py flake8`.  See:
#  * http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
#  * https://github.com/getsentry/raven-python/blob/master/setup.py
import multiprocessing
assert multiprocessing  # silence flake8


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        if isinstance(self.pytest_args, str):
            # pytest requires arguments as a list or tuple even if singular
            self.pytest_args = [self.pytest_args]
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read(fname):
    """
    Utility function to read the README file.
    :rtype : String
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='omero-user-token',
      python_requires='>=3.6',
      version=version.getVersion(),
      description='OMERO user token management system',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10'
      ],
      keywords='',
      author='Glencoe Software, Inc.',
      author_email='info@glencoesoftware.com',
      url='https://github.com/glencoesoftware/omero-user-token',
      packages=find_packages(),
      zip_safe=True,
      include_package_data=True,
      platforms='any',
      setup_requires=['flake8'],
      install_requires=[
          'click==7.0',
          'configparser==4.0.2',
          'omero-py>5.6',
      ],
      tests_require=[],
      cmdclass={'test': PyTest},
      data_files=[],
      entry_points={
          'console_scripts': [
              'omero_user_token = omero_user_token.cli.omero_user_token:main',
          ]
      }
      )
