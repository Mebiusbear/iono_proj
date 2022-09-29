from distutils.core import setup
 
from Cython.Build import cythonize
 
setup(name='legendre', ext_modules=cythonize('legendre.pyx'),)