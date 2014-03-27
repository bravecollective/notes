from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='bravenotes',
      version=version,
      description="Notepad system",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Felix Gustavsson',
      author_email='felix@fantas.in',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      namespace_packages = ['brave'],
      
      install_requires=[
          'web.py',
          'mongoengine',
          'markdown',
          'flup',
          'marrow.mailer',
          'requests==1.1.0',
      ]
)