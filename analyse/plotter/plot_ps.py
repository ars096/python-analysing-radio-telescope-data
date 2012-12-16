#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

import aplpy
import pylab

test = '/Users/nishimura/work/data/temp/test_data/test_ii.fits'


def s(*args, **kwargs):
    import pylab
    fig = pylab.figure()
    bbox = fig.add_subplot(*args, **kwargs).get_position()
    subplot = (bbox.x0, bbox.y0, bbox.width, bbox.height)
    pylab.close(fig)
    return subplot


fig = pylab.figure()
f = aplpy.FITSFigure(test, figure=fig, subplot=s(221))
f.show_colorscale()
f.show_colorbar()
f = aplpy.FITSFigure(test, figure=fig, subplot=s(222))
f.show_colorscale()
f.show_colorbar()
f = aplpy.FITSFigure(test, figure=fig, subplot=s(223))
f.show_colorscale()
f.show_colorbar()
pylab.show()
