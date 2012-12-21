#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

def qlook_skydip(dirpath):
    import os
    import pylab
    import analyse
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
        ana_data.append(analyse_skydip.analyse_skydip(hdu))
    # plot 
    name = f.split('_')[2]
    pylab.rcParams['legend.fontsize']=9
    ax = analyse.draw_skydip(ana_data[0],show=False,iso='12CO H',color='b')
    ax = analyse.draw_skydip(ana_data[2],ax=ax,show=False,iso='13CO H',color='g')
    ax = analyse.draw_skydip(ana_data[4],ax=ax,show=False,iso='C18O H',color='c')
    ax = analyse.draw_skydip(ana_data[1],ax=ax,show=False,iso='12CO V',color='r')
    ax = analyse.draw_skydip(ana_data[3],ax=ax,show=False,iso='13CO V',color='m')
    ax = analyse.draw_skydip(ana_data[5],ax=ax,show=False,iso='C18O V',color='y')
    ax.set_title('skydip on results ' + name)
    ax.legend()
    pylab.savefig('qlook_skydip_' + name + '_.png')
    pylab.close(ax.figure)
    return

