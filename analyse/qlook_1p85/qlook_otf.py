#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""


def qlook_otf(dirpath, filesave=False, reduct=True):
    import os
    import time
    import pylab
    import analyse
    import functools

    if dirpath[-1]!='/': dirpath += '/'
    files = sorted(os.listdir(dirpath))

    if len(files)<7:
        print('6 FITS files are required.')
        print(files)
        return

    qdir = dirpath + 'qlook/'
    if not os.path.exists(qdir):
        os.mkdir(qdir)


    fits12 = []
    fits13 = []
    fits18 = []
    # file check
    for f in files:
        if not f.endswith('fits'): continue
        if f.find('qlook')!=-1: continue
        if f.find('12CO')!=-1: fits12.append(f)
        if f.find('13CO')!=-1: fits13.append(f)
        if f.find('C18O')!=-1: fits18.append(f)
        continue

    name = fits12[0].split('_12CO_')[0]
    flag_ex = '.qlook.flag.fits'

    if reduct:
        os.system('python %s %s %s'%(__file__, dirpath+fits12[0], qdir))
        os.system('python %s %s %s %s'%(__file__, dirpath+fits12[1], qdir, qdir+fits12[0][:-5]+flag_ex))
        os.system('python %s %s %s'%(__file__, dirpath+fits13[0], qdir))
        os.system('python %s %s %s %s'%(__file__, dirpath+fits13[1], qdir, qdir+fits13[0][:-5]+flag_ex))
        os.system('python %s %s %s'%(__file__, dirpath+fits18[0], qdir))
        os.system('python %s %s %s %s'%(__file__, dirpath+fits18[1], qdir, qdir+fits18[0][:-5]+flag_ex))
        pass

    def plot(i, pol):
        ii12 = analyse.loadfits(qdir+fits12[i][:-5]+'.qlook.ii.fits')
        ii13 = analyse.loadfits(qdir+fits13[i][:-5]+'.qlook.ii.fits')
        ii18 = analyse.loadfits(qdir+fits18[i][:-5]+'.qlook.ii.fits')
        rms12 = analyse.loadfits(qdir+fits12[i][:-5]+'.qlook.rms.fits')
        rms13 = analyse.loadfits(qdir+fits13[i][:-5]+'.qlook.rms.fits')
        rms18 = analyse.loadfits(qdir+fits18[i][:-5]+'.qlook.rms.fits')
        sp12 = analyse.loadfits(qdir+fits12[i][:-5]+'.qlook.data.fits')
        sp13 = analyse.loadfits(qdir+fits13[i][:-5]+'.qlook.data.fits')
        sp18 = analyse.loadfits(qdir+fits18[i][:-5]+'.qlook.data.fits')
        fig = pylab.figure(figsize=(25,25))
        fig.suptitle(name, fontsize=22)
        plot = analyse.custom_draw_map(figure=fig, xspacing=0.2, yspacing=0.2,
                                       tick_labels_size=12, colorber_font_size=11, show=False)
        splt = functools.partial(analyse.draw_otf_spectrum, figure=fig, tick_labels_size=12,
                                 xlim=(-150,150), show=False)
        plot(ii12, subplot=331, title='12CO(2-1): mom0')
        plot(ii13, subplot=331+3, title='13CO(2-1): mom0')
        plot(ii18, subplot=331+6, title='C18O(2-1): mom0')
        plot(rms12, subplot=332, title='12CO(2-1): rms')
        plot(rms13, subplot=332+3, title='13CO(2-1): rms')
        plot(rms18, subplot=332+6, title='C18O(2-1): rms')
        splt(sp12, subplot=333, title='12CO(2-1): spectrum')
        splt(sp13, subplot=333+3, title='13CO(2-1): spectrum')
        splt(sp18, subplot=333+6, title='C18O(2-1): spectrum')
        fig.savefig(dirpath+name+'_%s_test.png'%(pol), dpi=70)
        pylab.close(fig)

    plot(0, 'H')
    plot(1, 'V')
    return


def easy_analyse(fitspath, output_dir, flag=None, plot=False, save=False):
    import analyse
    print('make_cube: %s'%(fitspath.split('/')[-1]))
    raw_data = analyse.loadfits(fitspath)
    cw_data = analyse.makespec(raw_data)

    if flag is None:
        fitted_data, flag = analyse.basefit(cw_data)
    else:
        flag = analyse.loadfits(flag)
        fitted_data = analyse.basefit_flag(cw_data, None, flag)
        pass
    convolved_data = analyse.convolve(fitted_data, 2)
    fitted_data = analyse.basefit_flag(convolved_data, None, flag)

    ii = analyse.make_2d_map(fitted_data, flag)
    rms = analyse.make_2d_map(fitted_data, flag, 'rms')

    if save:
        savepath = output_dir + fitspath.split('/')[-1].split('.fits')[0]
        analyse.savefits(fitted_data, savepath+'.qlook.data.fits', clobber=True)
        analyse.savefits(flag, savepath+'.qlook.flag.fits', clobber=True)
        analyse.savefits(ii, savepath+'.qlook.ii.fits', clobber=True)
        analyse.savefits(rms, savepath+'.qlook.rms.fits', clobber=True)
        pass

    if plot:
        savepath = output_dir + fitspath.split('/')[-1].split('.fits')[0]
        isotope = fitspath.split('_')[-2]
        plot = analyse.custom_draw_map(figure=(8,8), xspacing=0.2, yspacing=0.2,
                                       tick_labels_size=12, colorber_font_size=11, show=False)
        plot(ii, title='mom0: '+isotope).save(savepath+'.qlook.ii.png')
        plot(rms, title='rms: '+isotope).save(savepath+'.qlook.rms.png')
        analyse.draw_otf_spectrum(fitted_data, figure=(12,5), title='spectra: '+isotope,
                                  show=False).savefig(savepath+'.qlook.spectrum.png')
        pass

    raw_data.data = None
    cw_data.data = None
    return fitted_data, flag

if __name__ =='__main__':
    import sys
    if len(sys.argv)>=3:
        path = sys.argv[1]
        out = sys.argv[2]
        if len(sys.argv)>=4:
            flag_path = sys.argv[3]
        else: flag_path = None

        easy_analyse(path, out, flag_path, plot=True, save=True)
        pass
