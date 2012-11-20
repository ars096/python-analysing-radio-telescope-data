#! /usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""
Documents
"""

def makespec(hdu):
    obs_mode = hdu.data['OBSMODE'][0].upper()

    if obs_mode=='PS':
        return makespec_ps(hdu)
    elif obs_mode=='OTF':
        return makespec_otf(hdu)


def makespec_ps(hdu):
    def nearest_index(target, indices):
        return indices[numpy.array((indices - target)**2.).argmin()]

    import analyse
    import time
    import datetime
    import numpy
    import pyfits

    hot_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='HOT')[0]
    off_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='OFF')[0]
    on_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='ON')[0]
    on_coord_all = numpy.array((hdu.data['CRVAL2'][on_indices],
                                hdu.data['CRVAL3'][on_indices])).T
    on_coord_list = numpy.array({str(coord): coord for coord in on_coord_all}.values())

    fits_cube_list = []
    for x, y in on_coord_list:
        Ta_list = []
        xy_indices = numpy.where((hdu.data['CRVAL2']==x)&(hdu.data['CRVAL3']==y))
        for on_index in xy_indices[0]:
            hot_index = nearest_index(on_index, hot_indices)
            off_index = on_index - 1
            on_data = hdu.data['DATA'][on_index]
            off_data = hdu.data['DATA'][off_index]
            hot_data = hdu.data['DATA'][hot_index]
            hot_temp = hdu.data['THOT'][hot_index]
            Ta = (on_data - off_data)/(hot_data - off_data) * hot_temp
            Ta_list.append(Ta)
            continue
        Ta_list = numpy.array(Ta_list)

        timestamp = datetime.datetime.strptime(hdu.data['DATE-OBS'][0], '%Y-%m-%dT%H:%M:%S')
        nx = len(Ta_list)
        ny = 1
        nz = len(Ta_list[0])
        if hdu.data['COORDSYS'][2].lower()=='b1950':
            ctype1 = 'RA---CAR'
            ctype2 = 'DEC--CAR'
            cunit1 = 'deg'
            cunit2 = 'deg'
            equinox = 1950
        elif hdu.data['COORDSYS'][2].lower()=='j2000':
            ctype1 = 'RA---CAR'
            ctype2 = 'DEC--CAR'
            cunit1 = 'deg'
            cunit2 = 'deg'
            equinox = 2000
        elif hdu.data['COORDSYS'][2].lower()=='galactic':
            ctype1 = 'GLON-CAR'
            ctype2 = 'GLAT-CAR'
            cunit1 = 'deg'
            cunit2 = 'deg'
            equinox = 2000

        fits_cube = pyfits.PrimaryHDU()
        h = fits_cube.header
        h.update('SIMPLE', 'T')
        h.update('BITPIX', -32)
        h.update('NAXIS', 3)
        h.update('NAXIS1', nx)
        h.update('NAXIS2', ny)
        h.update('NAXIS3', nz)
        h.update('DATE', timestamp.strftime('%Y-%m-%d'))
        h.update('BUNIT', 'K')
        h.update('CTYPE1', ctype1)
        h.update('CUNIT1', cunit1)
        h.update('CRVAL1', hdu.data['CRVAL2'][2])
        h.update('CRPIX1', 0)
        h.update('CDELT1', 0)
        h.update('CTYPE2', ctype2)
        h.update('CUNIT2', cunit2)
        h.update('CRVAL2', hdu.data['CRVAL3'][2])
        h.update('CRPIX2', 0)
        h.update('CDELT2', 0)
        h.update('CTYPE3', 'VELO-LSR')
        h.update('CUNIT3', 'm/s')
        h.update('CRVAL3', hdu.data['CRVAL1'][0])
        h.update('CRPIX3', hdu.data['CRPIX1'][0])
        h.update('CDELT3', hdu.data['CDELT1'][0]*1000.)
        h.update('EQUINOX', equinox)
        h.update('_OBSERVE', hdu.data['OBSERVER'][0])
        h.update('_OBJECT', hdu.data['OBJECT'][0])
        h.update('_OBS-MOD', hdu.data['OBSMODE'][0])
        h.update('_OBS-DAT', hdu.data['DATE-OBS'][0])
        h.update('_OBS-EXP', hdu.data['EXPOSURE'][2])
        h.update('_OBS-AZ', hdu.data['AZIMUTH'][0])
        h.update('_OBS-EL', hdu.data['ELEVATIO'][0])
        h.update('_OFF-COO', hdu.data['COORDSYS'][off_indices[0]])
        h.update('_OFF-X', hdu.data['CRVAL2'][off_indices[0]])
        h.update('_OFF-Y', hdu.data['CRVAL3'][off_indices[0]])
        h.add_history('created by pyanalyse %s'%analyse.__version__)
        h.add_history('pyanalyse.makespec: generate Ta* data set (mode:PS)')
        h.add_history('pyanalyse.makespec: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
        fits_cube.data = Ta_list.T.reshape(nz, ny, nx)
        fits_cube_list.append(fits_cube)
        continue

    return fits_cube_list


def makespec_otf(hdu):
    pass