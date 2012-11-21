#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

__version__ = '0.2.a'

from basefunc.fits_io import loadfits
from basefunc.fits_io import savefits
from basefunc.makespec import makespec
from basefunc.baseline_fit import basefit
from basefunc.spectrum import get_tpeak as tpeak
from basefunc.sumspec import sumspec
