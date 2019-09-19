from setuptools import setup

setup(name='fin_benefits',
    version='0.1.0',
    #scripts=['fin_benefits/benefits.py'],   
	install_requires=['numpy'],#And any other dependencies required
	packages=setuptools.find_packages(),
	
    # metadata to display on PyPI
    author="Antti Tanskanen",
    author_email="antti.tanskanen@ek.fi",
    description="Finnish earning-related social security as a Python module",
    keywords="social-security earnings-related",
    #url="http://example.com/HelloWorld/",   # project home page, if any
    #project_urls={
    #    "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #    "Documentation": "https://docs.example.com/HelloWorld/",
    #    "Source Code": "https://code.example.com/HelloWorld/",
    #},
    #classifiers=[
    #    'License :: OSI Approved :: Python Software Foundation License'
    #]      
)
