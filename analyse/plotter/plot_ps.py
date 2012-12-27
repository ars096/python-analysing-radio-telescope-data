#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""


def s(*args, **kwargs):
    import pylab
    fig = pylab.figure()
    bbox = fig.add_subplot(*args, **kwargs).get_position()
    subplot = (bbox.x0, bbox.y0, bbox.width, bbox.height)
    pylab.close(fig)
    return subplot

def draw_ps_raw(raw, figure=None, subplot=111, title='', grid=True,
                      font_family=None, tick_labels_size=9, show=True):
    import analyse
    import analyse.plotter
    import pylab
    import matplotlib
    import numpy

    def_font_size = matplotlib.rcParams['font.size']
    def_font_family = matplotlib.rcParams['font.family']
    matplotlib.rcParams['font.size'] = tick_labels_size
    if font_family is not None: matplotlib.rcParams['font.family'] = font_family

    if figure is None:
        figure = pylab.figure()
    else:
        show = False

    if type(subplot) is int:
        subplot = analyse.plotter.get_subplot(subplot)
    elif type(subplot) in [list, tuple]:
        if len(subplot) == 3:
            subplot = analyse.plotter.get_subplot(subplot)

    crval = raw.data['crval1'][0]
    crpix = raw.data['crpix1'][0]
    cdelt = raw.data['cdelt1'][0]
    num = len(raw.data['data'][0])
    v = crval+(numpy.arange(num)-crpix+1)*cdelt

    ax = figure.add_axes(subplot)
    #[ax.plot(v, s) for s in spectra]
    [ax.plot(v, s) for s in raw.data['DATA']]
    ax.grid(grid)
    ax.set_title(title)

    if show:
        pylab.show()

    matplotlib.rcParams['font.size'] = def_font_size
    matplotlib.rcParams['font.family'] = def_font_family
    return figure

def draw_ps_spectrum(cube, figure=None, subplot=111, title='', grid=True,
                      font_family=None, tick_labels_size=9, show=True, *args, **kwargs):
    import analyse
    import analyse.plotter
    import pylab
    import matplotlib

    def_font_size = matplotlib.rcParams['font.size']
    def_font_family = matplotlib.rcParams['font.family']
    matplotlib.rcParams['font.size'] = tick_labels_size
    if font_family is not None: matplotlib.rcParams['font.family'] = font_family

    if figure is None:
        figure = pylab.figure()
    else:
        show = False

    if type(subplot) is int:
        subplot = analyse.plotter.get_subplot(subplot)
    elif type(subplot) in [list, tuple]:
        if len(subplot) == 3:
            subplot = analyse.plotter.get_subplot(subplot)

    nz, ny, nx = cube.data.shape
    spectra = cube.data.T.reshape(nx*ny, nz)
    v = analyse.generate_axis(cube, axis=3) / 1000.

    ax = figure.add_axes(subplot)
    [ax.plot(v, s) for s in spectra]
    ax.grid(grid)
    ax.set_title(title)

    if show:
        pylab.show()

    matplotlib.rcParams['font.size'] = def_font_size
    matplotlib.rcParams['font.family'] = def_font_family
    return figure

def draw_ss_spectrum(cube, flag, figure=None, subplot=111, title='', grid=True,
                      font_family=None, tick_labels_size=9, show=True, *args, **kwargs):
    import analyse
    import analyse.plotter
    import pylab
    import numpy
    import matplotlib

    tpeak, rms = analyse_ss(cube, flag)

    def_font_size = matplotlib.rcParams['font.size']
    def_font_family = matplotlib.rcParams['font.family']
    matplotlib.rcParams['font.size'] = tick_labels_size
    if font_family is not None: matplotlib.rcParams['font.family'] = font_family

    if figure is None:
        figure = pylab.figure()
    else:
        show = False

    if type(subplot) is int:
        subplot = analyse.plotter.get_subplot(subplot)
    elif type(subplot) in [list, tuple]:
        if len(subplot) == 3:
            subplot = analyse.plotter.get_subplot(subplot)

    nz, ny, nx = cube.data.shape
    spectra = cube.data.T.reshape(nx*ny, nz)
    v = analyse.generate_axis(cube, axis=3) / 1000.

    ax = figure.add_axes(subplot)
    [ax.plot(v, s) for s in spectra]
    ax.grid(grid)
    ax.set_title(title)
    """
    if fits_params['MOLECULE']=='12CO': tmb = float(sslist['tmb12'])
    elif fits_params['MOLECULE']=='13CO': tmb = float(sslist['tmb13'])
    elif fits_params['MOLECULE']=='C18O': tmb = float(sslist['tmb18'])
    else: pass
    """
    # 判断の参考に参考にTmbが○％のところに線を引く
    """
    xs = float(sslist['v_center']) - float(sslist['v_width'])/2.
    xe = float(sslist['v_center']) + float(sslist['v_width'])/2.
    """
    ###### atodekesu #####
    xs = -41.       #
    xe = 55.        #
    tmb = 40.       #
    ###### atodekesu #####
    percents = numpy.arange(50, 101, 10)
    percent_lines = tmb * percents / 100.
    [pylab.axhline(y=_y, color='r', linestyle='--', linewidth=2, alpha=0.5) for _y in percent_lines]
    [ax.text(xs, _y, str(_p)+'%') for _y, _p in zip(percent_lines, percents)]
    ax.set_ylim(-2, tmb*1.2)
    ax.set_ylabel('Ta* [K]')
    ax.set_xlabel('km/s')
    ax.set_xlim(xs, xe)
    #ax.set_title('%s %s' % (fits_params['OBJECT'], fits_params['DATE-OBS']))
    ax.annotate('Tpeak=%.2f [K]\nTmb=%.2f [K]\neff.=%.2f\nTrms=%.2f [K]'%(tpeak, tmb, tpeak/tmb, rms), xy=(.65,.85), xycoords='axes fraction')

    """
    if str(fits_params['BACKEND'])[-1]==1: direction='H'
    elif str(fits_params['BACKEND'])[-1]==2: direction='V'
    else: pass
    """

    if show:
        pylab.show()

    matplotlib.rcParams['font.size'] = def_font_size
    matplotlib.rcParams['font.family'] = def_font_family
    return figure

def analyse_ss(cube, flag):
    import numpy

    g = lambda x, mu, sig: 1/numpy.sqrt(2*numpy.pi*sig**2) * numpy.exp(-(x-mu)**2/(2*sig**2.))
    x = numpy.arange(len(cube.data))
    mu = len(cube.data)/2
    sig = 20/(2*numpy.sqrt(2*numpy.log(2)))
    g0 = g(x, mu, sig)  #コンボリューション用のガウシアンを生成 
    g0 /= numpy.sum(g0)  #規格化

    nz, ny, nx = cube.data.shape
    spectra = cube.data.copy().T.reshape(nx*ny, nz)
    spectrum = spectra[0]
    spectrum[numpy.isnan(spectrum)] = 0
    spectrum[numpy.isinf(spectrum)] = 0
    sd = numpy.convolve(spectrum, v=g0, mode='same')  #コンボリューション
    d_sd = [sd[i+1]-sd[i] for i,d_ in list(enumerate(sd))[:-1]]  #微分
    dd_sd = [d_sd[i+1]-d_sd[i] for i,d_ in list(enumerate(d_sd))[:-1]]  #微分
    # 観測された標準天体のピーク温度のチャンネルを算出(2回微分を行ったときの極小値)
    ddmin_ind = numpy.where(dd_sd==numpy.min(dd_sd))[0][0] - 1
    # 観測された標準天体のピーク温度を算出(上で求めたチャンネルの温度と、前後2点の値との平均をとっている)
    tpeak = numpy.average(spectrum[ddmin_ind-2:ddmin_ind+3])

    # --- rmsを求める ---
    flags = flag.data.copy().T.reshape(nx*ny, nz)
    spectra[numpy.where(flags!=0)] = 0
    spectra[numpy.isnan(spectra)] = 0
    spectra[numpy.isinf(spectra)] = 0
    rms = [numpy.sqrt(numpy.sum(spectra[i,:]**2)/float(nz)) for i in range(len(spectra))][0]

    print('tpeak: %.3f rms: %.3f'%(tpeak,rms))

    return tpeak, rms

def draw_ps(raw=None, cube=None, suptitle='', show=True,
             *args, **kwargs):
    import pylab

    fig = pylab.figure(figsize=(10,8))
    fig.suptitle(suptitle)

    #plot = custom_draw_map(figure=fig, show=False)
    draw_ps_raw(raw, figure=fig, subplot=231, title='raw', *args, **kwargs)
    draw_ps_spectrum(cube, figure=fig, subplot=234, title='spectra', *args, **kwargs)


    if show:
        pylab.show()

    return fig
