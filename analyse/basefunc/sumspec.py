#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
Documents
"""

def sumspec(hdus):
    import pyfits

    if isinstance(hdus, pyfits.PrimaryHDU):
        hdus = [hdus,]

    obsmode = hdus[0].header.get('_OBS-MOD')

    if obsmode.upper()=='PS':
        return sumspec_ps(hdus)
    elif obsmode.upper()=='OTF':
        return sumspec_otf(hdus)


def sumspec_ps(hdus):
    import numpy
    import pyfits

    d = [numpy.average(hdu.data[:,0,:], axis=1) for hdu in hdus]
    sumd = numpy.average(d, axis=0).reshape(len(d[0]), 1, 1)

    header = hdus[0].header.copy()
    sum_hdu = pyfits.PrimaryHDU(sumd, header)
    return sum_hdu

def sumspec_otf(hdus):
    # 今のところotfに対応していないかも
    import numpy
    import pyfits

    d = [numpy.average(hdu.data[:,0,:], axis=1) for hdu in hdus]
    sumd = numpy.average(d, axis=0).reshape(len(d[0]), 1, 1)

    header = hdus[0].header.copy()
    sum_hdu = pyfits.PrimaryHDU(sumd, header)
    return sum_hdu
