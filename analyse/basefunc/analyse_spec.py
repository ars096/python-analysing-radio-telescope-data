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

def make_2d_map(cube, flag=None, axis='v', detection_mode=''):
    import numpy

    print('make_2d_map: axis=%s'%(axis))

    nz, ny, nx = cube.data.shape
    
    if flag is None:
        flag = numpy.zeros((nz, ny, nx))

    if axis.lower() == 'rms':
        return make_rms_map(cube, flag, axis, detection_mode='')
    else:
        return make_integ_map(cube, flag, axis, detection_mode='')


def make_integ_map(cube, flag=None, axis='v', detection_mode=''):
    import numpy, pyfits, time
    import scipy.integrate as integrate
    
    nz, ny, nx = cube.data.shape
    
    if axis in ['v', 'V', 'z', 'Z']:
        #integ = numpy.zeros((ny, nx))
        #for i in range(nx):
        #    for j in range(ny):
        #        integ[j,i] = numpy.sum(cube.data[numpy.where(flag.data[:,j,i] == 1),j,i])
        dcube = cube.data.copy()
        dcube[numpy.where(flag.data!=1)] = 0
        dcube[numpy.isnan(dcube)] = 0
        dcube[numpy.isinf(dcube)] = 0
        integ = numpy.sum(dcube, axis=0)*(cube.header['DELT3']/1000.)

        header = cube.header.copy()
        header.pop('NAXIS3')
        header.pop('CRVAL3')
        header.pop('CRPIX3')
        header.pop('CDELT3')
        header.pop('CUNIT3')
        header.pop('CTYPE3')
        header.update('NAXIS', 2)
        header.update('BUNIT', 'K km/s')
        header.add_history('pyanalyse.make2dmap: generate integrated intensity (X-Y 2d data)')
        header.add_history('pyanalyse.make2dmap: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
        integ_hdu = pyfits.PrimaryHDU(integ, header)
    elif axis in ['x', 'X']:
        integ = numpy.zeros((nz, ny))
        for i in range(ny):
            for j in range(nz):
                integ[j,i] = numpy.sum(j,i,cube.data[numpy.where(flag.data[j,i,:] == 1)])
        
        header = cube.header.copy()
        header.pop('NAXIS1')
        header.pop('CRVAL1')
        header.pop('CRPIX1')
        header.pop('CDELT1')
        header.pop('CUNIT1')
        header.pop('CTYPE1')
        header.update('NAXIS', 2)
        header.add_history('pyanalyse.make2dmap: generate integrated intensity (Y-V 2d data)')
        header.add_history('pyanalyse.make2dmap: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
        integ_hdu = pyfits.PrimaryHDU(integ, header)
    elif axis in ['y', 'Y']:
        integ = numpy.zeros((nz, nx))
        for i in range(nx):
            for j in range(nz):
                integ[j,i] = numpy.sum(j,cube.data[numpy.where(flag.data[j,i,:] == 1)],i)
        
        header = cube.header.copy()
        header.pop('NAXIS2')
        header.pop('CRVAL2')
        header.pop('CRPIX2')
        header.pop('CDELT2')
        header.pop('CUNIT2')
        header.pop('CTYPE2')
        header.update('NAXIS', 2)
        header.add_history('pyanalyse.make2dmap: generate integrated intensity (X-V 2d data)')
        header.add_history('pyanalyse.make2dmap: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
        integ_hdu = pyfits.PrimaryHDU(integ, header)
    else:pass
    
    return integ_hdu

def make_rms_map(cube, flag=None, axis='v', detection_mode=''):
    import numpy, pyfits, time
    
    nz, ny, nx = cube.data.shape
    
    rms = numpy.zeros((ny, nx))
    for i in range(nx):
        for j in range(ny):
            rms[j,i] = numpy.sqrt(numpy.sum(cube.data[numpy.where(flag.data[:,j,i] == 0),j,i]**2.)/len(numpy.where(flag.data[:,j,i] == 0)[0]))
    
    header = cube.header.copy()
    header.pop('NAXIS3')
    header.pop('CRVAL3')
    header.pop('CRPIX3')
    header.pop('CDELT3')
    header.pop('CUNIT3')
    header.pop('CTYPE3')
    header.update('NAXIS', 2)
    header.add_history('pyanalyse.make2dmap: generate rms 2d data')
    header.add_history('pyanalyse.make2dmap: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
    rms_hdu = pyfits.PrimaryHDU(rms, header)
    return rms_hdu


def convolve(data, width, kernel_type='gauss'):
    import time
    import numpy
    import scipy.signal
    import pyfits
    import sys

    print('convolve: width=%.2f'%(width)),
    sys.stdout.flush()

    if kernel_type.lower()=='gauss': kernel_func = gaussian_kernel
    else: kernel_func = gaussian_kernel

    d = numpy.array(data.data, dtype=numpy.float32)
    k = kernel_func(width)

    cd = numpy.array([scipy.signal.fftconvolve(_d, k, 'same') for _d in d], dtype=numpy.float32)

    header = data.header.copy()
    header.add_history('pyanalyse.convolve: convolved type=%s width=%.1f'%(kernel_func, width))
    header.add_history('pyanalyse.convolve: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))

    convolved_hdu = pyfits.PrimaryHDU(cd, header)
    print('')
    return convolved_hdu


def gaussian_kernel(hpbw, dim=2):
    import numpy
    from numpy import log as ln
    from numpy import sqrt
    sigma = hpbw / 2. / sqrt(2 * ln(2))
    sigma2 = 2 * sigma**2.
    s = int(hpbw/2. * 3 + 1)
    if dim == 1:
        x = numpy.mgrid[-s:s+1]
        g = numpy.exp(-(x ** 2 / sigma2))
    elif dim == 2:
        x, y = numpy.mgrid[-s:s+1, -s:s+1]
        g = numpy.exp(-(x ** 2 / sigma2 + y ** 2 / sigma2))
    else:
        return None
    return numpy.array(g/g.sum(), dtype=numpy.float32)
