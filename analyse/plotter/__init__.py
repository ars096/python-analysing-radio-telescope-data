#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""


def get_subplot(*args, **kwargs):
    import pylab
    fig = pylab.figure()
    bbox = fig.add_subplot(*args, **kwargs).get_position()
    subplot = (bbox.x0, bbox.y0, bbox.width, bbox.height)
    pylab.close(fig)
    return subplot

