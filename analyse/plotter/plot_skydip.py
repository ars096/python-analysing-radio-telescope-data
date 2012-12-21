#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

"""
Documents
"""

def draw_skydip(data, ax=None, color='b', shape='o', iso = '', show=True):
    import pylab
    tau = data[0]
    tsys = data[1]
    r2 = data[2]
    sec_z = data[3]
    hot_sky = data[4]
    fitdata = data[5]
    #plot
    if ax is None:
        print(ax)
        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.grid()
        ax.set_ylabel('log((Phot-Psky)/Phot)')
        ax.set_xlabel('secZ')
    else:
        print(ax)
        ax = ax
    ax.plot(sec_z, hot_sky, color + shape , markersize=7)
    ax.plot(sec_z, fitdata, color + '-', label='%s, tau = %.2f, Tsys* = %.2f, R^2 = %.3f' %(iso, tau, tsys, r2))
    if show:
        pylab.show()
    return ax
