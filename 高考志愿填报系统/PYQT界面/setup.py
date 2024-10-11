# PYD打包【可以打包但是缺少C++环境】
# pip install setuptools
from setuptools import setup
from Cython.Build import cythonize
setup(
    name='tmp_debug',
    ext_modules=cythonize("main.py"),
)