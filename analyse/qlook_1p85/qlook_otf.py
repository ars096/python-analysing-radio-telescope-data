#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""


def qlook_otf(dirpath, filesave=False):
    import os
    import pylab
    import analyse

    if dirpath[-1]!='/': dirpath += '/'
    files = sorted(os.listdir(dirpath))

    if len(files)<7:
        print('6 FITS files are required.')
        print(files)
        return

    fits_files = []
    # file check
    for f in files:
        if f.split('_')[0]!='otf':
            continue
        if f.split('.')[-1]!='fits':
            continue
        if f.split('.')[-3]=='qlook':
            continue
        fits_files.append(f)
        continue

    name = files[0].split('_12CO_H.fits')[0]

    for f in fits_files:
        os.system('python %s %s'%(__file__, dirpath+f))
        continue

    isotope = ['12CO', '13CO', 'C18O']
    fig = pylab.figure()
    fig.suptitle(name)
    for i, f in enumerate(fits_files[::2]):
        _name = dirpath+f.split('.fits')[0]
        cube = analyse.loadfits(_name+'.qlook.data.fits')
        ii = analyse.loadfits(_name+'.qlook.ii.fits')
        rms = analyse.loadfits(_name+'.qlook.rms.fits')
        analyse.draw_map(ii, figure=fig, subplot=331+3*i, title='mom0: '+isotope[i], show=False)
        analyse.draw_map(rms, figure=fig, subplot=332+3*i, title='rms: '+isotope[i], show=False)
        analyse.draw_otf_spectrum(cube, figure=fig, subplot=333+3*i, title='spectra: '+isotope[i], show=False)
        continue
    fig.savefig(dirpath+name+'_H.png')

    fig = pylab.figure()
    fig.suptitle(name)
    for i, f in enumerate(files[1::2]):
        _name = dirpath+f.split('.fits')[0]
        cube = analyse.loadfits(_name+'.qlook.data.fits')
        ii = analyse.loadfits(_name+'.qlook.ii.fits')
        rms = analyse.loadfits(_name+'.qlook.rms.fits')
        analyse.draw_map(ii, figure=fig, subplot=331+3*i, title='mom0: '+isotope[i], show=False)
        analyse.draw_map(rms, figure=fig, subplot=332+3*i, title='rms: '+isotope[i], show=False)
        analyse.draw_otf_spectrum(cube, figure=fig, subplot=333+3*i, title='spectra: '+isotope[i], show=False)
        continue
    fig.savefig(dirpath+name+'_V.png')
    return


def easy_analyse(fitspath, save=False):
    import analyse
    print('make_cube: %s'%(fitspath.split('/')[-1]))
    raw_data = analyse.loadfits(fitspath)
    cw_data = analyse.makespec(raw_data)
    fitted_data, flag = analyse.basefit(cw_data)
    convolved_data = analyse.convolve(fitted_data, 2)
    fitted_data, flag = analyse.basefit(convolved_data, 'auto', convolve=3)
    ii = analyse.make_2d_map(fitted_data, flag)
    rms = analyse.make_2d_map(fitted_data, flag, 'rms')

    savepath = fitspath.split('.fits')[0]
    if save:
        analyse.savefits(fitted_data, savepath+'.qlook.data.fits', clobber=True)
        analyse.savefits(flag, savepath+'.qlook.flag.fits', clobber=True)
        analyse.savefits(ii, savepath+'.qlook.ii.fits', clobber=True)
        analyse.savefits(rms, savepath+'.qlook.rms.fits', clobber=True)
        pass

    raw_data.data = None
    cw_data.data = None
    del(raw_data)
    del(cw_data)
    return fitted_data

if __name__ =='__main__':
    import sys
    if len(sys.argv)==2:
        path = sys.argv[1]
        easy_analyse(path, save=True)
        pass
