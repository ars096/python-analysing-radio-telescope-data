#! /usr/bin/env python2.6
#-*- coding: utf-8 -*-

"""
Documents
"""

def analyse_radiop(hdu):
    import analyse
    import numpy
    import pylab
    
    data = hdu.data
    head = hdu.header
    
    scandata_one = []
    scandata = []
    rdata = None
    offdata = None
    ondata = None

    for fits_params in data:
        if fits_params['SOBSMODE']=='HOT':
            rdata = fits_params['DATA']
            continue
        elif fits_params['SOBSMODE']=='OFF':
            if offdata!=None:
                scandata.append(scandata_one)
                scandata_one = []
            else: pass
            offdata = fits_params['DATA']
            continue
        elif fits_params['SOBSMODE']=='ON':
            ondata = fits_params['DATA']
            ta = (fits_params['THOT']) * (ondata - offdata) / (rdata - offdata)
            new_fits_params = {'DATA': ta,
                               'OTFSCANN': fits_params['OTFSCANN'],
                               'AZIMUTH': fits_params['AZIMUTH'],
                               'ELEVATIO': fits_params['ELEVATIO'],
                               'OBJECT': fits_params['OBJECT'],
                               'BACKEND': fits_params['BACKEND'],
                               'MOLECULE': fits_params['MOLECULE']}
            scandata_one.append(new_fits_params)
            continue
        else: pass
        continue
    scandata.append(scandata_one)

    def _div(x, y):
        '''
        yの微分をとる。
        '''
        y = numpy.array(y)
        x = numpy.array(x)
        y_div = y[1:] - y[:-1]
        x_center = (x[1:] + x[:-1]) / 2.
        return x_center, y_div

    def _calc_params(fits_params):
        import numpy, scipy.optimize
        data = numpy.array([fitsp['DATA'] for fitsp in fits_params])[::-1]
        data = numpy.average(data,axis=1)
        x = numpy.linspace(-(len(data)-1)/2., (len(data)-1)/2., len(data))
        x_div, d_div = _div(x, data)
        x_detail = numpy.linspace(-(len(data)-1)/2., (len(data)-1)/2., len(data)*5)
        x_div_detail, d_div = _div(x_detail, data) 
        fitfunc = lambda p, x: max(d_div)*numpy.exp(-4*numpy.log(2)*(x-p[0])**2/p[1]**2)+min(d_div)*numpy.exp(-4*numpy.log(2)*(x-p[2])**2/p[3]**2)
        errfunc = lambda p, x, y: fitfunc(p, x) - y
        p0 = [x_div[d_div.argmax()-2], 3., x_div[d_div.argmin()-2], 3.]
        p1, success = scipy.optimize.leastsq(errfunc, p0[:], args=(x_div, d_div))
        left_line = p1[0]
        right_line = p1[2]
        center_line = (left_line + right_line) / 2.
        fit = fitfunc(p1, x_div_detail)
        az = fits_params[0]['AZIMUTH']
        el = fits_params[0]['ELEVATIO']
        deg = fits_params[0]['OTFSCANN']
        target = fits_params[0]['OBJECT']
        calc_params = {'data':[x,data], 'div_data':[x_div,d_div], 'fit_data':[x_div_detail,fit],
                       'fitparams':p1, 'center':center_line, 'left':left_line, 'right':right_line,
                       'Az':az, 'El':el, 'scan':deg, 'target':target}
        return calc_params
    
    analysed_params = []
    for _f in scandata:
        calced = _calc_params(_f)
        analysed_params.append(calced)

    return analysed_params
