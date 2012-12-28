#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""


def draw_map(data, figure=None, subplot=111,
             vmin=0, vmax=None, pmin=None, pmax=100.0, cmap='default',
             smooth=None, kernel='gauss', grid=True, gcolor='k',
             contour=True, levels=11, ccmap='None', ccolors='k',
             title='', xaxis_label=True, yaxis_label=True,
             xspacing=1, yspacing=1,
             tick_labels_xformat='ddd.d', tick_labels_yformat='dd.d',
             tick_labels_size=9, colorber_font_size=8,
             font_family=None,
             save=None, show=True):
    import analyse
    import analyse.plotter
    import aplpy
    import matplotlib.figure
    import pylab
    if not isinstance(figure, matplotlib.figure.Figure):
        if figure is None:
            figure = pylab.figure()
        else:
            figure = pylab.figure(figsize=figure)
    else:
        show = False

    if type(subplot) is int:
        subplot = analyse.plotter.get_subplot(subplot)
    elif type(subplot) in [list, tuple]:
        if len(subplot) == 3:
            subplot = analyse.plotter.get_subplot(subplot)

    fits_figure = aplpy.FITSFigure(data, figure=figure, subplot=subplot)
    fits_figure.show_colorscale(vmin=vmin, vmax=vmax, pmin=pmin, pmax=pmax,
                                cmap=cmap, smooth=smooth, kernel=kernel)
    if contour:
        fits_figure.show_contour(data, levels=levels, cmap=ccmap, colors=ccolors,
                                 smooth=smooth, kernel=kernel)

    if grid:
        fits_figure._figure.axes[-1].grid(True, color=gcolor)

    fits_figure.show_colorbar()

    if title!='':
        fits_figure._figure.axes[-2].set_title(title, size=tick_labels_size+1)

    if not xaxis_label:
        fits_figure.hide_xaxis_label()
    elif type(xaxis_label)==str:
        fits_figure.axis_labels.set_xtext(xaxis_label)

    if not yaxis_label:
        fits_figure.hide_yaxis_label()
    elif type(yaxis_label)==str:
        fits_figure.axis_labels.set_ytext(yaxis_label)

    fits_figure.set_tick_xspacing(xspacing)
    fits_figure.set_tick_yspacing(yspacing)
    fits_figure.set_tick_labels_xformat(tick_labels_xformat)
    fits_figure.set_tick_labels_yformat(tick_labels_yformat)

    # font config
    fits_figure.axis_labels.set_font(family=font_family, size=tick_labels_size)
    fits_figure.tick_labels.set_font(family=font_family, size=tick_labels_size)
    fits_figure.colorbar.set_font(family=font_family, size=colorber_font_size)

    if save is not None:
        fits_figure.save(save)

    if show:
        pylab.show()

    return fits_figure


def custom_draw_map(**kwargs):
    import functools
    return functools.partial(draw_map, **kwargs)


def draw_otf_spectrum(cube, figure=None, subplot=111, title='', grid=True,
                      font_family=None, tick_labels_size=9, xlim=None, ylim=None,
                      show=True, *args, **kwargs):
    import time
    import numpy
    import analyse
    import analyse.plotter
    import matplotlib.figure
    import matplotlib.colors
    import pylab
    t0 = time.time()
    print('[%f] -- %f'%(time.time(), time.time()-t0))
    if not isinstance(figure, matplotlib.figure.Figure):
        if figure is None:
            figure = pylab.figure()
        else:
            figure = pylab.figure(figsize=figure)
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
    #[ax.plot(v, s, '.b', ms=1, mew=0, alpha=0.1) for s in spectra]
    xd = numpy.array(list(v) * len(spectra))
    yd = spectra.ravel()
    yd[numpy.isnan(yd)] = 0
    histmap, histx, histy = pylab.histogram2d(xd, yd, bins=501)
    histmap = histmap.T
    histmap[numpy.where(histmap==0)] = 0.3
    histmap = numpy.log10(histmap)
    histX, histY = numpy.meshgrid(histx, histy)
    ax.pcolormesh(histX, histY, histmap, vmax=3.3)
    ax.grid(grid)
    ax.set_title(title, size=tick_labels_size+1)
    if xlim is not None: ax.set_xlim(*xlim)
    else: ax.set_xlim(xd.min(), xd.max())
    if ylim is not None: ax.set_ylim(*ylim)
    else: ax.set_ylim(yd.min(), yd.max())
    tx = ax.get_xticks()
    ty = ax.get_yticks()
    ax.set_xticklabels(tx, size=tick_labels_size)
    ax.set_yticklabels(ty, size=tick_labels_size)

    if show:
        pylab.show()

    print('[%f] -- %f'%(time.time(), time.time()-t0))
    return figure


def draw_otf(cube, flag=None, ii=None, rms=None, suptitle='', show=True,
             *args, **kwargs):
    import pylab
    import analyse

    if ii is None: ii = analyse.make_2d_map(cube, flag)
    if rms is None: rms = analyse.make_2d_map(cube, flag, 'rms')

    fig = pylab.figure(figsize=(10,8))
    fig.suptitle(suptitle)

    plot = custom_draw_map(figure=fig, show=False)
    plot(ii, subplot=221, title='mom0', *args, **kwargs)
    plot(rms, subplot=222, title='rms', yaxis_label=False, *args, **kwargs)
    draw_otf_spectrum(cube, figure=fig, subplot=212, title='spectra', *args, **kwargs)

    if show:
        pylab.show()

    return fig
