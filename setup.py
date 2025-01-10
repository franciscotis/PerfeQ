from setuptools import setup

import naming_check.naming_check

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='perfeq',
    version=naming_check.VERSION,
    license='MIT License',
    author='Francisco Pereira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='franncisco.p@gmail.com',
    keywords='code quality analysis tool',
    description=u'A tool for code quality analysis ',
    packages=['perfeq'],
      )