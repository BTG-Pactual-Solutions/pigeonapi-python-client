from setuptools import setup, find_packages
import os
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []

if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
else:
    requirementPath = thelibFolder + '/pigeonapi-python-client.egg-info/requires.txt'
    if os.path.isfile(requirementPath):
        with open(requirementPath) as f:
            install_requires = f.read().splitlines()

description = "Python package containing several classes and data for extracting and manipulating market and trading data."

setup(
    name='pigeonapi-python-client',
    version='0.9',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="PigeonAPI powered by BTG Pactual Solutions",
    packages=find_packages(),
    url="https://github.com/BTG-Pactual-Solutions/pigeonapi-python-client",
    install_requires=install_requires,
    python_requires=">=3.7",
)