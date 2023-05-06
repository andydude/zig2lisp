#!/usr/bin/env python

from distutils.core import setup

setup(name='zig2lisp',
      version='0.6.0',
      description='Convert Zig to Lisp',
      author='Andrew Robbins',
      author_email='andjrob@gmail.com',
      url='https://github.com/andydude/zig2lisp',
      packages=['ds_read_zig', 'ds_write_zig'],
      scripts=['scripts/lisp2zig', 'scripts/zig2lisp']
     )
