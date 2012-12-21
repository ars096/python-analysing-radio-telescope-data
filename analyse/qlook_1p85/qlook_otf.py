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

    fits12 = []
    fits13 = []
    fits18 = []
    # file check
    for f in files:
        if not f.endwith('fits'): continue
        if f.split('.')[-3]=='qlook':
            continue
        fits_files.append(f)
        continue

    name = fits_files[0].split('_12CO_H.fits')[0]
    flag_path = dirpath+f[0]+'.qlook.flag.fits'

    os.system('python %s %s'%(__file__, dirpath+fits_files[0]))
    for f in fits_files:
        os.system('python %s %s %s'%(__file__, dirpath+f, dirpath+flag_path))
        continue

    isotope = ['12CO', '13CO', 'C18O']
    plot = analyse.custom_draw_map(xspacing=0.2, yspacing=0.2, tick_labels_size=7,
                                   colorber_font_size=6, show=False)

    fig = pylab.figure(figsize=(12,10))
    fig.suptitle(name)
    for i, f in enumerate(fits_files[::2]):
        _name = dirpath+f.split('.fits')[0]
        cube = analyse.loadfits(_name+'.qlook.data.fits')
        ii = analyse.loadfits(_name+'.qlook.ii.fits')
        rms = analyse.loadfits(_name+'.qlook.rms.fits')
        plot(ii, figure=fig, subplot=331+3*i, title='mom0: '+isotope[i])
        plot(rms, figure=fig, subplot=332+3*i, title='rms: '+isotope[i])
        analyse.draw_otf_spectrum(cube, figure=fig, subplot=333+3*i, title='spectra: '+isotope[i], show=False)
        continue
    fig.savefig(dirpath+name+'_H.png')
    pylab.close(fig)

    fig = pylab.figure(figsize=(12,10))
    fig.suptitle(name)
    for i, f in enumerate(fits_files[1::2]):
        _name = dirpath+f.split('.fits')[0]
        cube = analyse.loadfits(_name+'.qlook.data.fits')
        ii = analyse.loadfits(_name+'.qlook.ii.fits')
        rms = analyse.loadfits(_name+'.qlook.rms.fits')
        plot(ii, figure=fig, subplot=331+3*i, title='mom0: '+isotope[i])
        plot(rms, figure=fig, subplot=332+3*i, title='rms: '+isotope[i])
        analyse.draw_otf_spectrum(cube, figure=fig, subplot=333+3*i, title='spectra: '+isotope[i], show=False)
        continue
    fig.savefig(dirpath+name+'_V.png')
    pylab.close(fig)
    return


def easy_analyse(fitspath, flag=None, plot=False, save=False):
    import analyse
    print('make_cube: %s'%(fitspath.split('/')[-1]))
    raw_data = analyse.loadfits(fitspath)
    cw_data = analyse.makespec(raw_data)

    if flag is None:
        fitted_data, flag = analyse.basefit(cw_data)
        convolved_data = analyse.convolve(fitted_data, 2)
        fitted_data, flag = analyse.basefit(convolved_data, 'auto', convolve=3)
        pass

    ii = analyse.make_2d_map(fitted_data, flag)
    rms = analyse.make_2d_map(fitted_data, flag, 'rms')

    if save:
        savepath = fitspath.split('.fits')[0]
        analyse.savefits(fitted_data, savepath+'.qlook.data.fits', clobber=True)
        analyse.savefits(flag, savepath+'.qlook.flag.fits', clobber=True)
        analyse.savefits(ii, savepath+'.qlook.ii.fits', clobber=True)
        analyse.savefits(rms, savepath+'.qlook.rms.fits', clobber=True)
        pass

    if plot:
        savepath = fitspath.split('.fits')[0]
        analyse.draw_map(ii, vmin=0).save(savepath+'.qlook.ii.png')
        analyse.draw_map(rms, vmin=0).save(savepath+'.qlook.rms.png')
        pass

    raw_data.data = None
    cw_data.data = None
    return fitted_data, flag

if __name__ =='__main__':
    import sys
    if len(sys.argv)>=2:
        path = sys.argv[1]
        if len(sys.argv)>=3:
            flag_path = sys.argv[2]
        else: flag_path = None

        easy_analyse(path, flag_path, save=True)
        pass
