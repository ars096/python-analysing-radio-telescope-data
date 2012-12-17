#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

import analyse
import analyse.plotter

import pylab
import aplpy

def draw_map(data, figure=None, subplot=None,
             vmin=0, vmax=None, pmin=None, pmax=100.0, cmap='default',
             smooth=None, kernel='gauss', grid=True, gcolor='k',
             contour=True, levels=11, ccmap='None', ccolors='k',
             title='', xaxis_label=True, yaxis_label=True,
             xspacing=1, yspacing=1,
             tick_labels_xformat='ddd.d', tick_labels_yformat='dd.d',
             tick_labels_size=9, colorber_font_size=8,
             font_family=None,
             show=True):
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


def custom_map_plotter(**kwargs):
    import functools
    return functools.partial(draw_map, **kwargs)


def draw_otf_ii(data, flag=None, *args, **kwargs):
    if flag is None:
        data, flag = analyse.basefit(data)

    ii = analyse.make_2d_map(data, flag)

    return draw_map(ii, *args, **kwargs)


def draw_otf_rms(data, flag=None, *args, **kwargs):
    if flag is None:
        data, flag = analyse.basefit(data)

    rms = analyse.make_2d_map(data, flag, 'rms')

    return draw_map(rms, *args, **kwargs)


def draw_otf(ii=None, rms=None, cube=None, flag=None, suptitle='', show=True,
             *args, **kwargs):
    fig = pylab.figure(figsize=(10,5))
    fig.suptitle(suptitle)

    if ii is None:
        draw_otf_ii(cube, flag, figure=fig, subplot=121, title='mom0', show=False,
                    *args, **kwargs)
    else:
        draw_map(ii, figure=fig, subplot=121, title='mom0', show=False, *args, **kwargs)

    if rms is None:
        draw_otf_rms(cube, flag, figure=fig, subplot=122, title='rms', yaxis_label=False,
                     show=False, *args, **kwargs)
    else:
        draw_map(rms, figure=fig, subplot=122, title='rms', yaxis_label=False,
                 show=False, *args, **kwargs)

    if show:
        pylab.show()

    return fig
