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
from basefunc.baseline_fit import basefit_interactive
from basefunc.analyse_spec import make_2d_map
from basefunc.sumspec import sumspec

from basefunc.useful import generate_axis

from plotter.plot_otf import draw_map
from plotter.plot_otf import custom_draw_map
from plotter.plot_otf import draw_otf
from plotter.plot_otf import draw_otf_spectrum

