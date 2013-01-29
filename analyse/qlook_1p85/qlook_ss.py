#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""


def qlook_ss(dirpath, filesave=False, savepath='./'):
    import os
    import pylab
    import analyse

    if dirpath[-1]!='/': dirpath += '/'
    files = sorted(os.listdir(dirpath))

    if len(files)<10:
        print('6 FITS files are required.')
        print(files)
        return

    fits_files = []
    # file check
    for f in files:
        if f.split('_')[0]!='ps':
            continue
        if f.split('.')[-1]!='fits':
            continue
        if f.split('.')[-3]=='qlook':
            continue
        fits_files.append(f)
        continue

    name = files[4].split('_12CO_H.fits')[0]
    timestamp = dirpath.split('/')[-2]

    for f in fits_files:
        os.system('python %s %s'%(__file__, dirpath+f))
        continue

    isotope = ['12CO', '13CO', 'C18O']
    fig = pylab.figure(figsize=(20,12))
    fig.suptitle(name+'_H')
    for i, f in enumerate(fits_files[::2]):
        _name = dirpath+f.split('.fits')[0]
        raw = analyse.loadfits(_name+'.fits')
        d = analyse.makespec(raw)
        cube, flag = analyse.basefit(d[0])
        #cube = analyse.loadfits(_name+'.qlook.data.fits')
        #flag = analyse.loadfits(_name+'.qlook.flag.fits')
        analyse.draw_ps_raw(raw, figure=fig, subplot=231+i, title='raw: '+isotope[i], show=False)
        analyse.draw_ss_spectrum(cube, flag, figure=fig, subplot=234+i, title='spectrum: '+isotope[i], show=False)
        continue
    fig.savefig(savepath+'qlook_standardsource_'+timestamp+'_H.png')
    #pylab.show()

    fig = pylab.figure(figsize=(20,12))
    fig.suptitle(name+'_V')
    for i, f in enumerate(fits_files[1::2]):
        _name = dirpath+f.split('.fits')[0]
        raw = analyse.loadfits(_name+'.fits')
        d = analyse.makespec(raw)
        cube, flag = analyse.basefit(d[0])
        #cube = analyse.loadfits(_name+'.qlook.data.fits')
        #flag = analyse.loadfits(_name+'.qlook.flag.fits')
        analyse.draw_ps_raw(raw, figure=fig, subplot=231+i, title='raw: '+isotope[i], show=False)
        analyse.draw_ss_spectrum(cube, flag, figure=fig, subplot=234+i, title='spectrum: '+isotope[i], show=False)
        continue
    fig.savefig(savepath+'qlook_standardsource_'+timestamp+'_V.png')
    #pylab.show()
    return

def easy_analyse(fitspath, save=False, savepath='./'):
    import analyse
    print('make_cube: %s'%(fitspath.split('/')[-1]))
    raw_data = analyse.loadfits(fitspath)
    cw_data = analyse.makespec(raw_data)
    fitted_data, flag = analyse.basefit(cw_data)
    convolved_data = analyse.convolve(fitted_data, 2)
    fitted_data, flag = analyse.basefit(convolved_data, 'auto')

    savepath = savepath + fitspath.split('.fits')[0]
    if save:
        analyse.savefits(fitted_data, savepath+'.qlook.data.fits', clobber=True)
        analyse.savefits(flag, savepath+'.qlook.flag.fits', clobber=True)
        pass

    raw_data.data = None
    cw_data.data = None
    del(raw_data)
    del(cw_data)
    return fitted_data
