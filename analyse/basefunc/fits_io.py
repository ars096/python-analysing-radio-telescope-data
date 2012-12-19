#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
Documents
"""

def loadfits(fitspath):
    import pyfits

    print('loadfits: %s,'%(fitspath)),

    hdu = pyfits.open(fitspath)

    if hdu[0].header.has_key('extend'):
        print('type-->sdfits')
        return hdu[1]

    print('type-->simple fits')
    return hdu[0]


def savefits(hdu, path, clobber=False):
    print('savefits: %s, clobber=%s'%(path, clobber))
    hdu.writeto(path, clobber=clobber)
    return


