#! /usr/bin/env python
#-*- coding: utf-8 -*-


def basefit(hdu, mode='auto', *args, **kwargs):
    import time
    import numpy
    import pyfits

    if mode.lower()=='simple':
        fitfunc = basefit_simple
    elif mode.lower()=='auto':
        fitfunc = basefit_auto

    nz, ny, nx = hdu.data.shape
    crpix3 = hdu.header['CRPIX3']
    crval3 = hdu.header['CRVAL3']
    cdelt3 = hdu.header['CDELT3']
    v = (numpy.arange(nz) - crpix3) * cdelt3 + crval3
    spectra = hdu.data.copy().T.reshape(nx*ny, nz)
    fit_results = [fitfunc(spec, v, *args, **kwargs) for spec in spectra]
    fitted = numpy.array(fit_results)[:,0].reshape(nx, ny, nz).T
    emission_flag = numpy.array(fit_results)[:,1].reshape(nx, ny, nz).T

    header = hdu.header.copy()
    header.add_history('pyanalyse.basefit: generate fitted data (mode:%s)'%mode)
    header.add_history('pyanalyse.basefit: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))

    ef_header = hdu.header.copy()
    ef_header.add_history('pyanalyse.basefit: generate emission flag (mode:%s)'%mode)
    ef_header.add_history('pyanalyse.basefit: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
    return pyfits.PrimaryHDU(fitted, header), pyfits.PrimaryHDU(emission_flag, ef_header)


def basefit_simple(spect, v, fitting_part=None, degree=1):
    def nearest_index(target, indices):
        return numpy.array((indices - target)**2.).argmin()

    import numpy

    if fitting_part is None:
        #!! TODO: generate feasible fitting part automatically
        # 今のところ仮のfiting range 2012/11/1
        fitting_part = ((-100,-50), (50,100))
        pass

    fit_indices = []
    for start, end in fitting_part:
        start_ind = nearest_index(start*1000, v)
        end_ind = nearest_index(end*1000, v)
        if start_ind < end_ind: step = 1
        else: step = -1
        fit_indices.append(numpy.arange(start_ind, end_ind, step))
        continue

    fit_indices = numpy.concatenate(fit_indices)
    fitted_curve = numpy.polyfit(v[fit_indices], spect[fit_indices], deg=degree)
    fitted_spect = spect - numpy.polyval(fitted_curve, v)

    emission_flag = numpy.ones(len(spect))
    emission_flag[fit_indices] = 0

    return fitted_spect, emission_flag


def basefit_auto(spect, v):
    return spect

