#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

def get_tpeak(hdu, smooth_num=5):
    import numpy
    import pyfits

    nz, ny, nx = hdu.data.shape
    spec = hdu.data.copy().T.reshape(nx*ny, nz)
    tpeak = [_tpeak(s) for s in spec]
    tpeak = numpy.array(tpeak).reshape(nx, ny).T

    header = hdu.header.copy()
    header.pop('NAXIS3')
    header.update('NAXIS', 2)
    tpeak_hdu = pyfits.PrimaryHDU(tpeak, header)
    return tpeak_hdu

def _tpeak(spec, _smooth_num=5):
    import numpy

    spec[numpy.isnan(spec)] = 0.
    conv = numpy.ones(_smooth_num) / float(_smooth_num)
    smoothed = numpy.convolve(spec, conv, 'same')
    return smoothed.max()
