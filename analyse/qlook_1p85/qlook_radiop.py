#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""


def qlook_radiop(dirpath, savepath='./'):
    import numpy
    import os
    import pylab
    import analyse
    import analyse.basefunc.analyse_radiop
    import analyse.plotter.plot_radiop
    import pylab
    
    if dirpath[-1]!='/': dirpath += '/'
    files = sorted(os.listdir(dirpath))
    
    fits_files = []
    # file check
    for f in files:
        if f.split('.')[-1]!='fits':
            continue
        fits_files.append(f)
        continue
    fits_files.sort()
    # load analysed data
    ana_data = []
    for f in fits_files:
        hdu = analyse.loadfits(dirpath+f)
        ana_data.append(analyse.basefunc.analyse_radiop.analyse_radiop(hdu))
    
    d = ana_data
    
    #import plot_radiop
    fig = pylab.figure(figsize=(12,5))
    name = f.split('_')[2]
    target = d[0][0]['target']
    pylab.rcParams['legend.fontsize'] = 5
    pylab.rcParams['figure.subplot.hspace'] = 0.5
    pylab.rcParams['figure.subplot.wspace'] = 0.5
    pylab.rcParams['font.size'] = 6
    ax1,ax2,fig = analyse.plotter.plot_radiop.draw_radiop(d[0][0], iso = '12CO_H', color='b',fig=fig,ax1_plot=221, ax2_plot=223,show=False)
    ax1,ax2,fig = analyse.plotter.plot_radiop.draw_radiop(d[2][0], iso = '13CO_H', color='g',fig=fig,ax1=ax1, ax2=ax2,show=False)
    ax1,ax2,fig = analyse.plotter.plot_radiop.draw_radiop(d[4][0], iso = 'C18O_H', color='c',fig=fig,ax1=ax1, ax2=ax2,show=False)
    ax1,ax2,fig = analyse.plotter.plot_radiop.draw_radiop(d[1][0], iso = '12CO_V', color='r',fig=fig,ax1=ax1, ax2=ax2,show=False)
    ax1,ax2,fig = analyse.plotter.plot_radiop.draw_radiop(d[3][0], iso = '13CO_V', color='m',fig=fig,ax1=ax1, ax2=ax2,show=False)
    ax1,ax2,fig = analyse.plotter.plot_radiop.draw_radiop(d[5][0], iso = 'C18O_V', color='y',fig=fig,ax1=ax1, ax2=ax2,show=False)
    ax3 = None
    ax4 = None
    ax3,ax4,fig = analyse.plotter.plot_radiop.draw_radiop(d[0][1], iso = '12CO_H', color='b',fig=fig, ax1=ax3, ax2=ax4, ax1_plot=144, ax2_plot=143,show=False, vertical=True)
    ax3,ax4,fig = analyse.plotter.plot_radiop.draw_radiop(d[2][1], iso = '13CO_H', color='g',fig=fig,ax1=ax3, ax2=ax4,show=False, vertical=True)
    ax3,ax4,fig = analyse.plotter.plot_radiop.draw_radiop(d[4][1], iso = 'C18O_H', color='c',fig=fig,ax1=ax3, ax2=ax4,show=False, vertical=True)
    ax3,ax4,fig = analyse.plotter.plot_radiop.draw_radiop(d[1][1], iso = '12CO_V', color='r',fig=fig,ax1=ax3, ax2=ax4,show=False, vertical=True)
    ax3,ax4,fig = analyse.plotter.plot_radiop.draw_radiop(d[3][1], iso = '13CO_V', color='m',fig=fig,ax1=ax3, ax2=ax4,show=False, vertical=True)
    ax3,ax4,fig = analyse.plotter.plot_radiop.draw_radiop(d[5][1], iso = 'C18O_V', color='y',fig=fig,ax1=ax3, ax2=ax4,show=False, vertical=True)
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    fig.text(0.5,0.975, target + ' cross scan results ' + name, horizontalalignment='center',verticalalignment='top')
    pylab.savefig(savepath+'qlook_radiop_' + name + '.png')
    #pylab.savefig('qlook_radiop' + name + '.pdf')
    pylab.close(fig)
    return

