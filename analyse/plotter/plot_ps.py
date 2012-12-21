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
                      font_family=None, tick_labels_size=9, show=True):
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
