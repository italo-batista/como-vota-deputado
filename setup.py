from setuptools import setup, find_packages

setup(
  name = 'comovotadeputado',
  packages=find_packages(),
  version = '1.0',
  description = 'To describe',
  author = 'Italo Batista',
  author_email = 'italohmb@gmail.com',
  url = 'https://github.com/italo-batista/como-vota-deputado', 
  download_url = 'https://github.com/italo-batista/como-vota-deputado/archive/1.0.tar.gz',
  keywords = ['opendata', 'politicians', 'br'], 
  classifiers = [],
  install_requires=[
    'beaker',
    'pandas',
    'requests',
    'xmltodict',
    'mock',
    'nose',
    'enum'
  ],
  test_suite='nose.collector',
  tests_require=['nose'],
  include_package_data=True,
  zip_safe=False
)
