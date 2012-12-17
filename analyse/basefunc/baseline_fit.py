#! /usr/bin/env python
#-*- coding: utf-8 -*-


def basefit(hdu, mode='auto', *args, **kwargs):
    import time
    import numpy
    import pyfits

    if mode.lower()=='simple':
        fitfunc = basefit_simple
    elif mode.lower()=='auto':
        fitfunc = basefit_auto

    nz, ny, nx = hdu.data.shape
    crpix3 = hdu.header['CRPIX3']
    crval3 = hdu.header['CRVAL3']
    cdelt3 = hdu.header['CDELT3']
    v = (numpy.arange(nz) - crpix3) * cdelt3 + crval3
    spectra = hdu.data.copy().T.reshape(nx*ny, nz)
    fit_results = [fitfunc(spec, v, *args, **kwargs) for spec in spectra]
    fitted = numpy.array(fit_results)[:,0].reshape(nx, ny, nz).T
    emission_flag = numpy.array(fit_results)[:,1].reshape(nx, ny, nz).T

    header = hdu.header.copy()
    header.add_history('pyanalyse.basefit: generate fitted data (mode:%s)'%mode)
    header.add_history('pyanalyse.basefit: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))

    ef_header = hdu.header.copy()
    ef_header.add_history('pyanalyse.basefit: generate emission flag (mode:%s)'%mode)
    ef_header.add_history('pyanalyse.basefit: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
    return pyfits.PrimaryHDU(fitted, header), pyfits.PrimaryHDU(emission_flag, ef_header)


def basefit_simple(spect, v, fitting_part=None, degree=1, *args, **kwargs):
    import numpy

    if fitting_part is None:
        #!! TODO: generate feasible fitting part automatically
        # 今のところ仮のfiting range 2012/11/1
        fitting_part = ((-100,-50), (50,100))
        pass

    fit_indices = numpy.zeros(spect.shape)
    for start, end in fitting_part:
        start_ind = nearest_index(start*1000, v)
        end_ind = nearest_index(end*1000, v)
        if start_ind > end_ind:
            tmp = start_ind
            start_ind = end_ind
            end_ind = tmp

        fit_indices[start_ind:end_ind] = 1
        continue

    fit_indices[numpy.isnan(spect)] = 0
    fit_indices = numpy.where(fit_indices==1)
    #fit_indices = numpy.argsort(numpy.concatenate(fit_indices))
    fitted_curve = numpy.polyfit(v[fit_indices], spect[fit_indices], deg=degree)
    fitted_spect = spect - numpy.polyval(fitted_curve, v)

    emission_flag = numpy.ones(len(spect))
    emission_flag[fit_indices] = 0
    emission_flag[:numpy.min(fit_indices)] = -1
    emission_flag[numpy.max(fit_indices):] = -1

    return fitted_spect, emission_flag


def basefit_auto(spect, v, fitting_range=[None,None], degree=1,
                 smooth=5, nsig=1.2, maxittr=10):
    import numpy

    if fitting_range[0] is not None:
        smaller_ind = spect[numpy.where(v<fitting_range[0]*1000.)]
    else: smaller_ind = []
    if fitting_range[1] is not None:
        larger_ind =  spect[numpy.where(v>fitting_range[1]*1000.)]
    else: larger_ind = []

    fit_d = spect.copy()
    fit_d[smaller_ind] = 0
    fit_d[larger_ind] = 0
    fit_d = numpy.convolve(fit_d, numpy.ones(smooth)/float(smooth), 'same')
    fit_d[smaller_ind] = numpy.nan
    fit_d[larger_ind] = numpy.nan
    initial_rms = rms(fit_d)
    rms_history = [initial_rms]
    threshold = initial_rms
    for i in xrange(maxittr):
        d = fit_d.copy()
        d[numpy.where(d > threshold*nsig)] = numpy.nan
        next_rms = rms(d)
        rms_history.append(next_rms)
        if next_rms*nsig > threshold: break
        threshold = next_rms
        continue

    fit_indices = numpy.where(d==d)
    fitted_curve = numpy.polyfit(v[fit_indices], spect[fit_indices], deg=degree)
    fitted_spect = spect - numpy.polyval(fitted_curve, v)

    emission_flag = numpy.ones(len(spect))
    emission_flag[fit_indices] = 0

    return fitted_spect, emission_flag


def nearest_index(target, indices):
    return numpy.array((indices - target)**2.).argmin()

def rms(d):
    import numpy
    dd = d[numpy.where(d==d)]
    return numpy.sqrt(numpy.sum(dd**2.)/float(len(dd)))

def cut_small_sample(d, nsig=1, mincount=5, threshold=None, *args, **kwargs):
    dd = d.copy()
    if nsig==0: dd[numpy.where(dd<0)] = 0.
    else:
        if threshold is None: threshold = rms_itt(dd) * nsig
        dd[numpy.where(numpy.abs(dd)<threshold)] = 0.
        pass
    checking = []
    for i,_d in enumerate(dd):
        if _d == 0:
            if len(checking)==0: continue
            if len(checking)<=mincount:
                dd[checking] = 0
                pass
            checking = []
            continue
        checking.append(i)
        continue
    return dd


def basefit_interactive(data, flag):
    ibase = interactive_basefit(data, flag)
    ibase.generate_ii()
    ibase.generate_rms()
    ibase.start()
    return

class interactive_basefit(object):
    smooth = 1

    def __init__(self, cube, flag=None):
        self.cube = cube
        self.flag = flag
        self.shape = cube.data.shape
        self.size = cube.data.size
        self.nz = self.shape[0]
        self.ny = self.shape[1]
        self.nx = self.shape[2]
        pass

    def set_ii(self, ii):
        self.ii = ii
        return

    def set_rms(self, rms):
        self.rms = rms
        return

    def generate_flag(self):
        import analyse
        self.flag = analyse.basefit(self.cube)
        return

    def generate_ii(self):
        import analyse
        self.ii = analyse.make_2d_map(self.cube, self.flag)
        return

    def generate_rms(self):
        import analyse
        self.rms = analyse.make_2d_map(self.cube, self.flag, 'rms')
        return

    def _key_handler(self, event):
        key = event.key
        print('[%s]'%key),
        if key=='right': self._key_right()
        elif key=='left': self._key_left()
        elif key=='up': self._key_up()
        elif key=='down': self._key_down()
        elif key in ['h', '?']: self._key_h()
        elif key=='q': self._key_q()
        elif key=='b': self._key_b()
        elif key=='x': self._key_x()
        print('.')
        return

    def _key_right(self):
        self.current_position += 1
        self.check_current_position()
        return

    def _key_left(self):
        self.current_position -= 1
        self.check_current_position()
        return

    def _key_up(self):
        self.current_position += self.nx
        self.check_current_position()
        return

    def _key_down(self):
        self.current_position -= self.nx
        self.check_current_position()
        return

    def _key_h(self):
        import pylab
        print('-- help')
        print('right, left, up, down : move')
        print('h, ? : show help')
        print('q    : quit')
        print('b    : bindup')
        print('x    : set xlim')
        print('y    : set ylim')
        return

    def _key_q(self):
        import pylab
        print('quit'),
        pylab.close(self.fig)
        return

    def _key_b(self):
        self.smooth = int(raw_input('bindup: '))
        return

    def _key_x(self):
        return

    def _key_y(self):
        return

    def check_current_position(self):
        if self.current_position < 0:
            self.current_position = 0
        elif self.current_position >= self.size:
            self.current_position = self.size - 1
        print('currend_position = %d'%self.current_position),
        return

    def start(self):
        import matplotlib.animation
        import pylab
        import analyse

        self.current_position = 0

        self.fig = pylab.figure()
        analyse.draw_map(self.ii, figure=self.fig, subplot=221)
        self.ax1 = self.fig.axes[-2]
        analyse.draw_map(self.rms, figure=self.fig, subplot=222)
        self.ax2 = self.fig.axes[-2]
        self.line11, = self.ax1.plot([], [], 'w*', markersize=15)
        self.line21, = self.ax2.plot([], [], 'w*', markersize=15)
        self.ax3 = self.fig.add_subplot(212)
        self.ax3.set_xlim(0, self.nz)
        self.ax3.set_ylim(-5, 20)
        self.ax3.grid(True)
        self.line31, = self.ax3.plot([], [], 'b')
        self.line32, = self.ax3.plot([], [], 'c')
        self.fig.canvas.mpl_connect('key_press_event', self._key_handler)
        anime = matplotlib.animation.FuncAnimation(self.fig, self.refresh, frames=self._dummy_itt,
                                                   interval=50, blit=False)
        pylab.show()
        return

    def _dummy_itt(self):
        while True:
            yield 0

    def refresh(self, *args):
        import numpy
        import time
        x = self.current_position % self.nx
        y = self.current_position / self.nx
        spectrum = self.cube.data[:,y,x]
        spectrum = numpy.convolve(spectrum, numpy.ones(self.smooth)/float(self.smooth), 'same')
        flag = self.flag.data[:,y,x]
        self.line11.set_data([x+0.5,], [y+0.5,])
        self.line21.set_data([x+0.5,], [y+0,5,])
        self.line31.set_data(numpy.arange(len(spectrum)), spectrum)
        self.line32.set_data(numpy.where(flag==0)[0], spectrum[numpy.where(flag==0)])
        #self.fig.canvas.draw()
        return



