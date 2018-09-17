import os

from setuptools import setup, find_packages

requires = [
  'kubernetes==7.0.0',
]

setup(
    name='app',
    version='1.0',
    description='Proxy a specified port to a specified pod (single node service)',
    classifiers=[
      'Programming Language :: Python',
      'Framework :: Pyramid',
      'Topic :: Internet :: WWW/HTTP',
      'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Colin Chartier',
    author_email='colin@kubenow.com',
    url='https://kubenow.com',
    keywords='build ci deployment kubernetes',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
      'console_scripts': [
        'entrypoint = app.main:main',
      ],
    },
)
