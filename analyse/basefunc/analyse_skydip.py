#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

"""
=======================================
#analyse_skydip
 main-author: K.Tokuda
- - - - - - - - - - - - - - - - - - - -
[History]

2012/12/17 updated by K.Tokuda
---------------------------------------
"""

def analyse_skydip(hdu):
    import numpy
    data = hdu.data
    rdata = numpy.array(numpy.sum(data[0][5]))
    offdata = numpy.array([numpy.sum(data[d][5]) for d in range(1,6)])
    #calc sec_z & hot_sky data
    hot_sky = numpy.sort(numpy.log((rdata - offdata)/rdata))[::-1]
    sec_z = numpy.sort(1./numpy.cos(numpy.radians(90. - numpy.array(data['elevatio'][1:]))))
    #fitting
    fitfunc = numpy.polyfit(sec_z,hot_sky,1)
    fitline = numpy.poly1d(fitfunc)
    fitdata = fitline(sec_z)
    #calc params
    tau = -1.*(fitline(1.)-fitline(0.))
    tsys = (offdata[-1] * data[-1]['THOT'])/(rdata - offdata[-1])
    r2 = 1- sum((hot_sky - fitdata)**2) / sum((hot_sky - numpy.average(hot_sky))**2)

    return tau, tsys, r2, sec_z, hot_sky, fitdata
