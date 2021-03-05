import fnmatch
from setuptools import find_packages, setup, Extension
from setuptools.command.build_py import build_py as build_py_orig
from Cython.Build import cythonize


extensions = [
    Extension('fin_benefits.*', ['fin_benefits/benefits.py']),
]
cython_excludes = ['**/__init__.py']


def not_cythonized(tup):
    (package, module, filepath) = tup
    return any(
        fnmatch.fnmatchcase(filepath, pat=pattern) for pattern in cython_excludes
    ) or not any(
        fnmatch.fnmatchcase(filepath, pat=pattern)
        for ext in extensions
        for pattern in ext.sources
    )


class build_py(build_py_orig):
    def find_modules(self):
        modules = super().find_modules()
        return list(filter(not_cythonized, modules))

    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return list(filter(not_cythonized, modules))

setup(
    name='fin_benefits',
    version='1.0.0',
    packages=find_packages(),
    ext_modules=cythonize(extensions, exclude=cython_excludes,
                          compiler_directives={'language_level' : "3"}),
    cmdclass={'build_py': build_py},
    install_requires=['numpy'],
    
    # metadata to display on PyPI
    author="Antti Tanskanen",
    author_email="antti.tanskanen@ek.fi",
    description="Finnish earning-related social security as a Python module",
    keywords="social-security earnings-related"
)
