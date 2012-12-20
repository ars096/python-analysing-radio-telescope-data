#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

class key_handler(object):
    def __init__(self, dic):
        self.dict = dic
        pass

    def __call__(self, event):
        print('[%s]'%event.key),
        self.dict.get(event.key, self.dummy)()
        return

    def dummy(self):
        print("no funcs: to see help, enter 'h'")


def show_spectrum_simple(data, *args, **kwargs):
    view = viewer_spectrum_simple(data)
    if kwargs.has_key('colors'): view.set_colors(kwargs['colors'])
    view.start()
    return

def show_fittings_simple(data, flag, *args, **kwargs):
    view = viewer_fittings_simple(data, flag)
    if kwargs.has_key('colors'): view.set_colors(kwargs['colors'])
    view.start()
    return


class viewer_spectrum_simple(object):
    help_str = ''
    _key_handler = None

    def __init__(self, cube_list):
        import numpy
        import analyse

        self._init_key_mapping()

        if not type(cube_list) in [list, tuple]: cube_list = [cube_list,]
        self.original_cube_list = cube_list
        self.cube_list = self.original_cube_list
        shapes = numpy.array([cube.data.shape for cube in cube_list])
        self.nx = shapes[0][2]
        self.ny = shapes[0][1]
        self.size = self.nx * self.ny
        self.vels = [analyse.generate_axis(cube, axis=3)/1000. for cube in cube_list]
        self.velmin = numpy.min([v.min() for v in self.vels])
        self.velmax = numpy.max([v.max() for v in self.vels])

        self.colors = analyse.default_colors
        self.bindup_num = 1
        self.convolve = 0

        self.xmin = self.velmin
        self.xmax = self.velmax
        self.ymin = -5
        self.ymax = 20
        pass

    def set_colors(self, colors):
        self.colors = colors
        return

    def start(self, show=True):
        import matplotlib.animation
        import pylab

        def dummy_itt():
            while True:
                yield
                continue
            return

        self.current_position = 0

        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.grid(True)
        title = ax.set_title('')
        lines = [ax.plot([], [], color=self.colors[i]) for i in range(len(self.cube_list))]
        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)
        fig.canvas.mpl_connect('key_press_event', self._key_handler)

        self.fig = fig
        self.ax = ax
        self.title = title
        self.lines = lines

        anime = matplotlib.animation.FuncAnimation(fig, self._refresh, frames=dummy_itt,
                                                   interval=50, blit=False)
        if show: pylab.show()
        return

    def _refresh(self, *args):
        import numpy

        x = self.current_position % self.nx
        y = self.current_position / self.nx

        self.title.set_text('%d, (x=%d, y=%d)'%(self.current_position, x, y))

        for cube, line, vel in zip(self.cube_list, self.lines, self.vels):
            spectrum = cube.data[:,y,x]
            spectrum = numpy.convolve(spectrum,
                                      numpy.ones(self.bindup_num)/float(self.bindup_num),
                                      'same')
            line[0].set_data(vel, spectrum)
            continue
        return

    def _init_key_mapping(self):
        k = {
            # common functions
            # ----------------
            'h': self.help,
            '?': self.help,
            'q': self.quit,
            # move functions
            # --------------
            'right': self.move_right,
            'left': self.move_left,
            'up': self.move_up,
            'down': self.move_down,
            'm': self.move,
            # spectrum analyze functions
            # --------------------------
            'b': self.bindup,
            'c': self.convolve,
            # figure functions
            # ----------------
            'x': self.xlim,
            'y': self.ylim,
        }
        self._key_handler = key_handler(k)
        self.help_str = '[help] simple spectrum viewer\n'+\
                        '\n'+\
                        'mouse commands\n'+\
                        '==============\n'+\
                        '\n'+\
                        'keyboard commands\n'+\
                        '=================\n'+\
                        '\n'+\
                        'common functions\n'+\
                        '----------------\n'+\
                        'h, ? : show help\n'+\
                        'q    : quit. window will be closed\n'+\
                        '\n'+\
                        'move functions\n'+\
                        '--------------\n'+\
                        '->       : move right (next pixel)\n'+\
                        '<-       : move left (previous pixel)\n'+\
                        'up-key   : move up (next column pixel)\n'+\
                        'down-key : move down (previous column pixel)\n'+\
                        'm        : move to given pixel. \n'+\
                        '           enter serial number or coordinate value.\n'+\
                        '           [ex.] 1623 (for serial number)\n'+\
                        '           [ex.] 12, 30 (for pixel coordinate value)\n'+\
                        '\n'+\
                        'analyze functions\n'+\
                        '-----------------\n'+\
                        'b : bind up spectrum (frequency)\n'+\
                        '    enter bind number\n'+\
                        '    [ex.] 5\n'+\
                        'c : convolve spectrum (spatially)　<< unimplemented >>\n'+\
                        '\n'+\
                        'figure functions\n'+\
                        '----------------\n'+\
                        'x : set xlim'+\
                        '    enter xlim values in km/sec\n'+\
                        '    [ex.] -100, 100\n'+\
                        'y : set ylim'+\
                        '    enter ylim values in K\n'+\
                        '    [ex.] -1, 10\n'
        return

    def help(self):
        print(self.help_str)
        return

    def quit(self):
        import pylab
        print('quit')
        pylab.close(self.fig)
        self.fig = None
        return

    def move(self):
        m = eval(raw_input('move to: '))
        if type(m) in [tuple, list]:
            x = m[0]
            y = m[1]
            ind = None
        else:
            ind = m
            x = None
            y = None
        self._move(ind, x, y)
        return

    def move_right(self):
        self._move_delta(dx=1)
        return

    def move_left(self):
        self._move_delta(dx=-1)
        return

    def move_up(self):
        self._move_delta(dy=1)
        return

    def move_down(self):
        self._move_delta(dy=-1)
        return

    def _move(self, ind=None, x=None, y=None):
        if ind is None: ind = x + y * self.nx
        self.set_current_position(ind)
        return

    def _move_delta(self, dx=0, dy=0):
        dind = dx + dy * self.nx
        self.set_current_position(self.current_position + dind)
        return

    def set_current_position(self, index):
        if index < 0: index = 0
        elif index >= self.size: index = self.size - 1
        self.current_position = index
        print('current_position: %d'%(self.current_position))
        return

    def bindup(self):
        b = int(raw_input('bind num: '))
        self.bindup_num = b
        return

    def convolve(self):
        import analyse
        c = float(raw_input('convolve: '))
        convolved_data = [analyse.convolve(_d, c) for _d in self.original_cube_list]
        self.cube_list = convolved_data
        return

    def xlim(self):
        xlim = eval(raw_input('xlim: '))
        self.xmin = xlim[0]
        self.xmax = xlim[1]
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.figure.canvas.draw()
        return

    def ylim(self):
        ylim = eval(raw_input('ylim: '))
        self.ymin = ylim[0]
        self.ymax = ylim[1]
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.figure.canvas.draw()
        return


class viewer_fittings_simple(viewer_spectrum_simple):
    def __init__(self, cube, flag):
        viewer_spectrum_simple.__init__(self, cube)
        self.flag = flag
        pass

    def start(self, show=True):
        import matplotlib.animation
        import pylab

        def dummy_itt():
            while True:
                yield
                continue
            return

        self.current_position = 0

        fig = pylab.figure()
        ax = fig.add_subplot(111)
        ax.grid(True)
        title = ax.set_title('')
        lines = [ax.plot([], [], color=self.colors[i]) for i in range(len(self.cube_list))]
        flag_line = ax.plot([],[],'c')
        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)
        fig.canvas.mpl_connect('key_press_event', self._key_handler)

        self.fig = fig
        self.ax = ax
        self.title = title
        self.lines = lines
        self.flag_line = flag_line

        anime = matplotlib.animation.FuncAnimation(fig, self._refresh, frames=dummy_itt,
                                                   interval=50, blit=False)
        if show: pylab.show()
        return

    def _refresh(self, *args):
        import numpy

        x = self.current_position % self.nx
        y = self.current_position / self.nx

        self.title.set_text('%d, (x=%d, y=%d)'%(self.current_position, x, y))

        flag_flag = True
        for cube, line, vel in zip(self.cube_list, self.lines, self.vels):
            spectrum = cube.data[:,y,x]
            spectrum = numpy.convolve(spectrum,
                                      numpy.ones(self.bindup_num)/float(self.bindup_num),
                                      'same')
            line[0].set_data(vel, spectrum)
            if flag_flag:
                flag = numpy.where(self.flag.data[:,y,x] == 0)
                self.flag_line[0].set_data(vel[flag], spectrum[flag])
                flag_flag = False
                pass
            continue
        return

