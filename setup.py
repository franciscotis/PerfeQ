from setuptools import setup


with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='perfeq',
    version='1.0.0',
    license='MIT License',
    author='Francisco Pereira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='franncisco.p@gmail.com',
    keywords='integrated source code quality assessment tool',
    description=u'An integrated source code quality assessment tool focusing on adherence to programming language style conventions',
    packages=['perfeq'],
    install_requires=['pyfiglet', 'cpplint', 'pylint', 'naming-check'],
      )