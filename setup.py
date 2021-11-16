import fnmatch
from setuptools import find_packages, setup, Extension
from setuptools.command.build_py import build_py as build_py_orig


extensions = [
    Extension('fin_benefits.*', ['fin_benefits/benefits.py']),
]

setup(
    name='fin_benefits',
    version='1.2.0',
    packages=find_packages(),
    install_requires=['numpy'],
    
    # metadata to display on PyPI
    author="Antti Tanskanen",
    author_email="antti.tanskanen@ek.fi",
    description="Finnish earning-related social security as a Python module",
    keywords="social-security earnings-related"
)
