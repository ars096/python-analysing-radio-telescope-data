#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

import analyse
import analyse.plotter

import pylab
import aplpy

def draw_otf_ii(data, flag=None, figure=None, subplot=None,
                vmin=0, vmax=None, pmin=None, pmax=100.0, cmap='default',
                smooth=None, kernel='gauss', grid=True, gcolor='k',
                contour=True, levels=5, ccmap='None', ccolors='k',
                title='', tick_labels_xformat='ddd', tick_labels_yformat='dd',
                tick_labels_size=11, show=True):
    if flag is None:
        data, flag = analyse.basefit(data)

    ii = analyse.make_2d_map(data, flag)

    if figure is not None:
        figure = pylab.figure()

    if type(subplot) is int:
        subplot = analyse.plotter.get_subplot(subplot)
    elif type(subplot) in [list, tuple]:
        if len(subplot) == 3:
            subplot = analyse.plotter.get_subplot(subplot)

    fits_figure = aplpy.FITSFigure(ii, figure=figure, subplot=subplot)
    fits_figure.show_colorscale(vmin=vmin, vmax=vmax, pmin=pmin, pmax=pmax,
                                cmap=cmap, smooth=smooth, kernel=kernel)
    if contour:
        fits_figure.show_contour(ii, levels=levels, cmap=ccmap, colors=ccolors,
                                 smooth=smooth, kernel=kernel)

    if grid:
        fits_figure._figure.axes[-1].grid(True, color=gcolor)

    if title!='':
        fits_figure._figure.axes[-1].set_title(title)

    fits_figure.set_tick_labels_xformat(tick_labels_xformat)
    fits_figure.set_tick_labels_yformat(tick_labels_yformat)
    fits_figure.set_tick_labels_size(tick_labels_size)

    fits_figure.show_colorbar()

    return fits_figure

