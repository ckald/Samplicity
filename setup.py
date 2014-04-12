from samplicity.ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import os
import codecs
import re

here = os.path.abspath(os.path.dirname(__file__))

# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion


def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='samplicity',
      version=find_version('samplicity', 'samplicity.py'),
      description=".SFZ to .XI musical samples format converter",
      author="Andii Magalich",
      author_email="andrew.magalich@gmail.com",
      url="https://github.com/ckald/Samplicity",
      packages=find_packages(exclude=["contrib", "docs", "tests*"]),
      install_requires=["scikits.audiolab", "numpy"],
      long_description=open('README.rst').read(),
      entry_points={
          'console_scripts': [
              'samplicity=samplicity:main'
          ],
      }
      )
