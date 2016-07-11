# -*- coding: utf-8 -*-
import os
from setuptools import setup

project_dir = os.path.abspath(os.path.dirname(__file__))

long_descriptions = []
for rst in ('README.rst', 'LICENSE.rst'):
    with open(os.path.join(project_dir, rst), 'r') as f:
        long_descriptions.append(f.read())

setup(name='iotrelay-eagle',
      version='1.0.2',
      description='IoT Relay plugin for the Eagle™ Home Energy Gateway',
      long_description='\n\n'.join(long_descriptions),
      author='Emmanuel Levijarvi',
      author_email='emansl@gmail.com',
      url='https://github.com/eman/iotrelay-eagle',
      install_requires=['iotrelay', 'meter-reader'],
      license='BSD',
      py_modules=['eagle_gateway'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Utilities',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          ],
      keywords='Eagle Energy Gateway IoT electricity',
      entry_points={
          'iotrelay': ['source=eagle_gateway:Poll']
          })
