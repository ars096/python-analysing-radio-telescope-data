#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

def loadfits(fitspath):
    import pyfits

    hdu = pyfits.open(fitspath)

    if hdu[0].header.has_key('extend'):
        return hdu[1].data

    return hdu[0]
