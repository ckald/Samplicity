from setuptools import setup, find_packages
from samplicity.samplicity import __version__ as version

setup(name='samplicity',
      version=version,
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
