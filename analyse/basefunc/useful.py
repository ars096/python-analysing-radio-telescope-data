#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

def generate_axis(hdu, axis=1):
    """generate axis from fits_data object"""
    import numpy
    header = hdu.header
    crval = header.get('CRVAL%1d'%(axis))
    crpix = header.get('CRPIX%1d'%(axis))
    cdelt = header.get('CDELT%1d'%(axis))
    num = header.get('NAXIS%1d'%(axis))
    return crval+(numpy.arange(num)-crpix+1)*cdelt
