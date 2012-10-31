#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

data_dir = '../../../data/temp/test_data/'
test_rawdata = data_dir + 'test_raw.fits'
test_2ddata = data_dir + 'test_ii.fits'
test_3ddata = data_dir + 'test_cube.fits'


import analyse.basefunc.loadfits

import unittest

class Test_loadfits(unittest.TestCase):
    def test_load_rawdata(self):
        import pyfits.fitsrec
        d = analyse.basefunc.loadfits.loadfits(test_rawdata)
        self.assertIsInstance(d, pyfits.fitsrec.FITS_rec)

    def test_load_2ddata(self):
        import pyfits.hdu.image
        d = analyse.basefunc.loadfits.loadfits(test_2ddata)
        self.assertIsInstance(d, pyfits.hdu.image.PrimaryHDU)

    def test_load_3ddata(self):
        import pyfits.hdu.image
        d = analyse.basefunc.loadfits.loadfits(test_2ddata)
        self.assertIsInstance(d, pyfits.hdu.image.PrimaryHDU)

