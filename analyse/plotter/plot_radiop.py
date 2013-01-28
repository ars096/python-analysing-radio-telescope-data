#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

"""
Documents
"""

def draw_radiop(data, fig=None, ax1=None, ax2=None, ax1_plot=211, ax2_plot=212, color='b', shape='+', iso = '', show=True, vertical=False):
    import pylab
    x = data['data'][0]
    d = data['data'][1]
    dx = data['div_data'][0]
    ddata = data['div_data'][1]
    fx = data['fit_data'][0]
    fd = data['fit_data'][1]
    scan = data['scan']
    target = data['target']
    l = data['left']
    r = data['right']
    c = data['center']
    left_beam = data['fitparams'][1]
    right_beam = data['fitparams'][3]
    az = data['Az']
    el = data['El']
    def draw_lines(ax,data,l,r,c):
        upper_limit = max(data) * 1.3
        lower_limit = min(data) * 1.3
        if vertical is True:
            ax.plot((lower_limit,upper_limit), (l,l), '--' + color)
            ax.plot((lower_limit,upper_limit), (r,r), '--' + color)
            ax.plot((lower_limit,upper_limit), (c,c), '-' + color)
        else:
            ax.plot((l,l), (lower_limit,upper_limit), '--' + color)
            ax.plot((r,r), (lower_limit,upper_limit), '--' + color)
            ax.plot((c,c), (lower_limit,upper_limit), '-' + color)
        return
    if fig is None:
        print(fig)
        fig = pylab.figure()
    if ax1 is None:
        print(ax1,ax2)
        ax1 = fig.add_subplot(ax1_plot)
        ax1.grid()
        ax2 = fig.add_subplot(ax2_plot)
        ax2.grid()
        ax1.plot(None,None,'k',label='iso   pol  (left, center, right)')
        ax2.plot(None,None,'k',label='iso   pol Beam(left, right)')
        if vertical is True:
            ax2.set_title('                                                                    Scandirection = %.1f Error:%.3f Az, El = [%.2f, %.2f]' %(scan, c, az, el))
            ax1.set_xlabel('TA* [K]')
            ax1.set_ylabel('degree [arcmin]')
            ax2.set_xlabel('differential')
            ax2.set_ylabel('degree [arcmin]')
        else:            
            ax1.set_title('Scandirection = %.1f Error:%.3f Az, El = [%.2f, %.2f]' %(scan, c, az, el))
            ax1.set_ylabel('TA* [K]')
            ax1.set_xlabel('degree [arcmin]')
            ax2.set_ylabel('differential')
            ax2.set_xlabel('degree [arcmin]')
    else:
        print(ax1,ax2)
        ax1 = ax1
        ax2 = ax2
    if vertical is True:
        ax1.plot(d, x, color, label='%s (%.2f, %.2f, %.2f)' %(iso, l, c, r))
        draw_lines(ax1, d, l,r,c)
        ax2.plot(ddata, dx, color + shape)
        ax2.plot(fd, fx, color, label='%s Beam(%.2f, %.2f)' %(iso, left_beam, right_beam))
        draw_lines(ax2, ddata, l,r,c)
    else:
        ax1.plot(x, d, color, label='%s (%.2f, %.2f, %.2f)' %(iso, l, c, r))
        draw_lines(ax1, d, l,r,c)
        ax2.plot(dx, ddata, color + shape)
        ax2.plot(fx, fd, color, label='%s Beam(%.2f, %.2f)' %(iso, left_beam, right_beam))
        draw_lines(ax2, ddata, l,r,c)
    if show:
        pylab.show()
    return ax1, ax2, fig

