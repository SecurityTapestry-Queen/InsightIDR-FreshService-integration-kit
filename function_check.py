#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module performing Functional check for Python 3.10+ and FS_API secret"""

import sys
import os

FS_API = os.getenv('FS_API')


def function_check():
    """Functional Check"""
    print('Performing Function Check')
    if sys.version_info < (3, 10):
        sys.exit('Python 3.10+ Needed')
    if str(FS_API) == 'None':
        sys.exit('FS_API key missing')
    print('Function Check Succeeded')


if __name__ == '__main__':
    function_check()
