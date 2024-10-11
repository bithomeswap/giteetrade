#【预防反编译】pyd文件
# pip install tinyaes
# python setup.py build_ext --inplace
# # PYD打包【可以打包但是缺少C++环境】setup.py文件内容
# # pip install setuptools
# from setuptools import setup
# from Cython.Build import cythonize
# setup(
#     name='tmp_debug',
#     ext_modules=cythonize("main.py"),
# )