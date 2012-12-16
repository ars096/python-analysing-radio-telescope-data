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
    import numpy

    if fitting_part is None:
        #!! TODO: generate feasible fitting part automatically
        # 今のところ仮のfiting range 2012/11/1
        fitting_part = ((-100,-50), (50,100))
        pass

    fit_indices = numpy.zeros(spect.shape)
    for start, end in fitting_part:
        start_ind = nearest_index(start*1000, v)
        end_ind = nearest_index(end*1000, v)
        if start_ind > end_ind:
            tmp = start_ind
            start_ind = end_ind
            end_ind = tmp

        fit_indices[start_ind:end_ind] = 1
        continue

    fit_indices[numpy.isnan(spect)] = 0
    fit_indices = numpy.where(fit_indices==1)
    #fit_indices = numpy.argsort(numpy.concatenate(fit_indices))
    fitted_curve = numpy.polyfit(v[fit_indices], spect[fit_indices], deg=degree)
    fitted_spect = spect - numpy.polyval(fitted_curve, v)

    emission_flag = numpy.ones(len(spect))
    emission_flag[fit_indices] = 0
    emission_flag[:numpy.min(fit_indices)] = -1
    emission_flag[numpy.max(fit_indices):] = -1

    return fitted_spect, emission_flag


def basefit_auto(spect, v, fitting_range=[None,None], degree=1,
                 smooth=5, nsig=1.2, maxittr=10):
    import numpy

    if fitting_range[0] is not None:
        smaller_ind = spect[numpy.where(v<fitting_range[0]*1000.)]
    else: smaller_ind = []
    if fitting_range[1] is not None:
        larger_ind =  spect[numpy.where(v>fitting_range[1]*1000.)]
    else: larger_ind = []

    fit_d = spect.copy()
    fit_d[smaller_ind] = 0
    fit_d[larger_ind] = 0
    fit_d = numpy.convolve(fit_d, numpy.ones(smooth)/float(smooth), 'same')
    fit_d[smaller_ind] = numpy.nan
    fit_d[larger_ind] = numpy.nan
    initial_rms = rms(fit_d)
    rms_history = [initial_rms]
    threshold = initial_rms
    for i in xrange(maxittr):
        d = fit_d.copy()
        d[numpy.where(d > threshold*nsig)] = numpy.nan
        next_rms = rms(d)
        rms_history.append(next_rms)
        if next_rms*nsig > threshold: break
        threshold = next_rms
        continue

    fit_indices = numpy.where(d==d)
    fitted_curve = numpy.polyfit(v[fit_indices], spect[fit_indices], deg=degree)
    fitted_spect = spect - numpy.polyval(fitted_curve, v)

    emission_flag = numpy.ones(len(spect))
    emission_flag[fit_indices] = 0

    return fitted_spect, emission_flag


def nearest_index(target, indices):
    return numpy.array((indices - target)**2.).argmin()

def rms(d):
    import numpy
    dd = d[numpy.where(d==d)]
    return numpy.sqrt(numpy.sum(dd**2.)/float(len(dd)))

def cut_small_sample(d, nsig=1, mincount=5, threshold=None):
    dd = d.copy()
    if nsig==0: dd[numpy.where(dd<0)] = 0.
    else:
        if threshold is None: threshold = rms_itt(dd) * nsig
        dd[numpy.where(numpy.abs(dd)<threshold)] = 0.
        pass
    checking = []
    for i,_d in enumerate(dd):
        if _d == 0:
            if len(checking)==0: continue
            if len(checking)<=mincount:
                dd[checking] = 0
                pass
            checking = []
            continue
        checking.append(i)
        continue
    return dd
