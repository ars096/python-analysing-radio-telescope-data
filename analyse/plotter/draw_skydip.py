#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

"""
=======================================
#draw_skydip
 main-author: K.Tokuda
- - - - - - - - - - - - - - - - - - - -
[History]

2012/12/17 updated by K.Tokuda
---------------------------------------
"""

def draw_skydip(analyse_skydip, locX=0.6, locY=0.9, show=True):
    import pylab
    tau = analyse_skydip[0]
    tsys = analyse_skydip[1]
    r2 = analyse_skydip[2]
    sec_z = analyse_skydip[3]
    hot_sky = analyse_skydip[4]
    fitdata = analyse_skydip[5]
    #plot
    fig = pylab.figure()
    pylab.grid()
    pylab.ylabel('log((Phot-Psky)/Phot)')
    pylab.xlabel('secZ')
    pylab.plot(sec_z, hot_sky, 'o', markersize=7)
    pylab.plot(sec_z, fitdata)
    pylab.annotate('tau = %.2f, Tsys* = %.2f, R^2 = %.3f' %(tau, tsys, r2), \
                           xy=(locX,locY), xycoords='axes fraction',  size='small')
    if show:
        pylab.show()
    return fig
