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
             show=True):
    import analyse
    import analyse.plotter
    import aplpy
    import pylab
    if figure is None:
        figure = pylab.figure()
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
        fits_figure._figure.axes[-2].set_title(title)

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

    if show:
        pylab.show()

    return fits_figure


def custom_draw_map(**kwargs):
    import functools
    return functools.partial(draw_map, **kwargs)


def draw_otf_spectrum(cube, figure=None, subplot=111, title='', grid=True,
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


def draw_otf(ii=None, rms=None, cube=None, suptitle='', show=True,
             *args, **kwargs):
    import pylab

    fig = pylab.figure(figsize=(10,8))
    fig.suptitle(suptitle)

    plot = custom_draw_map(figure=fig, show=False)
    plot(ii, subplot=221, title='mom0', *args, **kwargs)
    plot(rms, subplot=222, title='rms', yaxis_label=False, *args, **kwargs)
    draw_otf_spectrum(cube, figure=fig, subplot=212, title='spectra', *args, **kwargs)

    if show:
        pylab.show()

    return fig
