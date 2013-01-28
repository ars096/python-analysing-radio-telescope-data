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
        ana_data.append(analyse.analyse_skydip(hdu))
    # plot 
    
    name = f.split('_')[2]
    pylab.rcParams['legend.fontsize']=5.5
    pylab.rcParams['figure.subplot.hspace']=0.5
    fig = pylab.figure(figsize=(8,5))
    ax = analyse.draw_skydip(ana_data[0],fig=fig,show=False,iso='12CO H',color='b')
    ax = analyse.draw_skydip(ana_data[2],fig=fig,ax=ax,show=False,iso='13CO H',color='g')
    ax = analyse.draw_skydip(ana_data[4],fig=fig,ax=ax,show=False,iso='C18O H',color='c')
    ax = analyse.draw_skydip(ana_data[1],fig=fig,ax=ax,show=False,iso='12CO V',color='r')
    ax = analyse.draw_skydip(ana_data[3],fig=fig,ax=ax,show=False,iso='13CO V',color='m')
    ax = analyse.draw_skydip(ana_data[5],fig=fig,ax=ax,show=False,iso='C18O V',color='y')
    ax.set_title('skydip results ' + name)
    ax.legend()

    #----------- plot raw data ---------------
    data12H = analyse.loadfits(dirpath+fits_files[0]).data
    data12V = analyse.loadfits(dirpath+fits_files[1]).data
    data13H = analyse.loadfits(dirpath+fits_files[2]).data
    data13V = analyse.loadfits(dirpath+fits_files[3]).data
    data18H = analyse.loadfits(dirpath+fits_files[4]).data
    data18V = analyse.loadfits(dirpath+fits_files[5]).data    
    print('-------sum 13 12 18 spectra------')
    
    import numpy
    x = numpy.linspace(0., 1.0, 16383)
    ax1 = fig.add_subplot(212)
    for  i in range(len(data12H)):
        d_H = numpy.concatenate((data18H[i]['data'], data12H[i]['data'], data13H[i]['data']))
        d_V = numpy.concatenate((data18V[i]['data'], data12V[i]['data'], data13V[i]['data']))
        ax1.plot(x, d_H,'b--')
        ax1.plot(x, d_V,'r--')
    ax1.set_ylabel('IF Power')
    ax1.set_xlabel('Frequency [GHz]')
    ax1.set_title('IFpower (blue:Hpol red:Vpol)')
    ax1.grid()
    
    pylab.savefig('qlook_skydip_' + name + '_.png')
    pylab.close(ax.figure)
    pylab.show()
    return

