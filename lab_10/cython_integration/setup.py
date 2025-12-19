from setuptools import setup, Extension
from Cython.Build import cythonize

# Флаги для OpenMP (параллельные вычисления)
compile_args = ['-O3']  # базовая оптимизация
link_args = []

# Проверяем платформу для OpenMP
import sys
if sys.platform.startswith('win'):
    # Для Windows
    compile_args.append('/openmp')
elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    # Для Linux/Mac
    compile_args.append('-fopenmp')
    link_args.append('-fopenmp')

extensions = [
    Extension(
        "integrate_cy",  # имя модуля
        sources=["integrate_cy.pyx"],  # исходный файл
        extra_compile_args=compile_args,  # флаги компиляции
        extra_link_args=link_args,  # флаги линковки
    ),
]

setup(
    name='integrate_cython',
    ext_modules=cythonize(
        extensions,  # передаем extensions внутрь cythonize
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'initializedcheck': False,
            'cdivision': True,
        },
        annotate=True,
    ),
)  # закрывающая скобка setup()