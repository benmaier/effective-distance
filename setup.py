from setuptools import setup

setup(name='effective-distance',
      version='0.1',
      description='Generates a radial layout for trees whose nodes are associated with a distance to the root.',
      url='https://github.com/benmaier/effective-distance',
      author='Benjamin F. Maier',
      author_email='bfmaier@physik.hu-berlin.de',
      license='MIT',
      packages=['effdist'],
      install_requires=[
          'numpy',
          'networkx',
      ],
      zip_safe=False)
