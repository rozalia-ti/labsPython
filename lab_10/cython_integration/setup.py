from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name='integrate_cython',
    ext_modules=cythonize(
        Extension("integrate_cy", sources=["integrate_cy.pyx"]),
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
        },
        annotate=True,
    ),
)