#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

def get_tpeak(spec):
    import numpy

    conv = numpy.ones(5) / float(conv)
    smoothed = numpy.convolve(spec, conv)
    return smoothed.max()

