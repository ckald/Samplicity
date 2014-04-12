from distutils.core import setup

setup(name='samplicity',
      version='0.5',
      description=".SFZ to .XI musical samples format converter",
      author="Andii Magalich",
      author_email="andrew.magalich@gmail.com",
      url="https://github.com/ckald/Samplicity",
      package_dir={'': 'source'},
      packages=[''],
      py_modules=['samplicity'],
      requires=["scikits.audiolab"],
      long_description=open('README.rst').read()
      )
