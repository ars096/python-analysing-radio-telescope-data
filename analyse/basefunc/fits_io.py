#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
Documents
"""

def loadfits(fitspath):
    import pyfits

    hdu = pyfits.open(fitspath)

    if hdu[0].header.has_key('extend'):
        return hdu[1]

    return hdu[0]


def savefits(hdu, path):
    hdu.writeto(path)
    return


