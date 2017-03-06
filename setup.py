from setuptools import setup, find_packages

setup(
    name='pyadf43x',
    version='0.1',
    packages=find_packages(),

    install_requires=['pyusb>=1.0.0'],

    author='Joel Holdsworth',
    author_email='joel@airwebreathe.org.uk',
    description='A package for automating AD4350/1 boards',
    license='GPLv2',
    url='http://github.com/jhol/pyadf435x'
)
