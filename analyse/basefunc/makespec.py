#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

def makespec(hdu):
    obs_mode = hdu.data['OBSMODE'][0].upper()

    if obs_mode=='PS':
        return makespec_ps(hdu)
    elif obs_mode=='OTF':
        return makespec_otf(hdu)


def makespec_ps(hdu):
    def nearest_index(target, indices):
        return indices[numpy.array((indices - target)**2.).argmin()]

    import analyse
    import time
    import datetime
    import numpy
    import pyfits

    hot_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='HOT')[0]
    off_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='OFF')[0]
    on_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='ON')[0]
    on_coord_all = numpy.array((hdu.data['CRVAL2'][on_indices],
                                hdu.data['CRVAL3'][on_indices])).T
    on_coord_list = numpy.array({str(coord): coord for coord in on_coord_all}.values())

    fits_cube_list = []
    for x, y in on_coord_list:
        Ta_list = []
        xy_indices = numpy.where((hdu.data['CRVAL2']==x)&(hdu.data['CRVAL3']==y))
        for on_index in xy_indices[0]:
            hot_index = nearest_index(on_index, hot_indices)
            off_index = on_index - 1
            on_data = hdu.data['DATA'][on_index]
            off_data = hdu.data['DATA'][off_index]
            hot_data = hdu.data['DATA'][hot_index]
            hot_temp = hdu.data['THOT'][hot_index]
            Ta = (on_data - off_data)/(hot_data - off_data) * hot_temp
            Ta_list.append(Ta)
            continue
        Ta_list = numpy.array(Ta_list)

        timestamp = datetime.datetime.strptime(hdu.data['DATE-OBS'][0], '%Y-%m-%dT%H:%M:%S')
        nx = len(Ta_list)
        ny = 1
        nz = len(Ta_list[0])
        if hdu.data['COORDSYS'][2].lower()=='b1950':
            ctype1 = 'RA---CAR'
            ctype2 = 'DEC--CAR'
            cunit1 = 'deg'
            cunit2 = 'deg'
            equinox = 1950
        elif hdu.data['COORDSYS'][2].lower()=='j2000':
            ctype1 = 'RA---CAR'
            ctype2 = 'DEC--CAR'
            cunit1 = 'deg'
            cunit2 = 'deg'
            equinox = 2000
        elif hdu.data['COORDSYS'][2].lower()=='galactic':
            ctype1 = 'GLON-CAR'
            ctype2 = 'GLAT-CAR'
            cunit1 = 'deg'
            cunit2 = 'deg'
            equinox = 2000

        fits_cube = pyfits.PrimaryHDU()
        h = fits_cube.header
        h.update('SIMPLE', 'T')
        h.update('BITPIX', -32)
        h.update('NAXIS', 3)
        h.update('NAXIS1', nx)
        h.update('NAXIS2', ny)
        h.update('NAXIS3', nz)
        h.update('DATE', timestamp.strftime('%Y-%m-%d'))
        h.update('BUNIT', 'K')
        h.update('CTYPE1', ctype1)
        h.update('CUNIT1', cunit1)
        h.update('CRVAL1', hdu.data['CRVAL2'][2])
        h.update('CRPIX1', 0)
        h.update('CDELT1', 0)
        h.update('CTYPE2', ctype2)
        h.update('CUNIT2', cunit2)
        h.update('CRVAL2', hdu.data['CRVAL3'][2])
        h.update('CRPIX2', 0)
        h.update('CDELT2', 0)
        h.update('CTYPE3', 'VELO-LSR')
        h.update('CUNIT3', 'm/s')
        h.update('CRVAL3', hdu.data['CRVAL1'][0])
        h.update('CRPIX3', hdu.data['CRPIX1'][0])
        h.update('CDELT3', hdu.data['CDELT1'][0]*1000.)
        h.update('EQUINOX', equinox)
        h.update('_OBSERVE', hdu.data['OBSERVER'][0])
        h.update('_OBJECT', hdu.data['OBJECT'][0])
        h.update('_OBS-MOD', hdu.data['OBSMODE'][0])
        h.update('_OBS-DAT', hdu.data['DATE-OBS'][0])
        h.update('_OBS-EXP', hdu.data['EXPOSURE'][2])
        h.update('_OBS-AZ', hdu.data['AZIMUTH'][0])
        h.update('_OBS-EL', hdu.data['ELEVATIO'][0])
        h.update('_OFF-COO', hdu.data['COORDSYS'][off_indices[0]])
        h.update('_OFF-X', hdu.data['CRVAL2'][off_indices[0]])
        h.update('_OFF-Y', hdu.data['CRVAL3'][off_indices[0]])
        h.add_history('created by pyanalyse %s'%analyse.__version__)
        h.add_history('pyanalyse.makespec: generate Ta* data set (mode:PS)')
        h.add_history('pyanalyse.makespec: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
        fits_cube.data = Ta_list.T.reshape(nz, ny, nx)
        fits_cube_list.append(fits_cube)
        continue

    return fits_cube_list


def makespec_otf(hdu):
    '''
    3次元 CUBE FITSを作成する
    作成後のCUBE FITS(3D)を返す
    
    引数 - hdu: 生データ (pyfits.fitsrec.FITS_rec)
    返り値 - fits_cube_list: チョッパーホイール後の3次元 CUBE FITS
    '''
    import analyse
    import time
    import datetime
    import numpy
    import pyfits
    
    off_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='OFF')[0]
    on_indices = numpy.where(hdu.data['SOBSMODE'].upper()=='ON')[0]
    
    Ta_list = hdu.data[on_indices]
    i = 0
    
    for fitsp in hdu.data:
        if fitsp['SOBSMODE'] == 'HOT':
            rdata = fitsp['DATA']
        elif fitsp['SOBSMODE'] == 'OFF':
            offdata = fitsp['DATA']
        elif fitsp['SOBSMODE'] == 'ON':
            ondata = fitsp['DATA']
            Ta_list[i]['DATA'] =  fitsp['THOT'] * (ondata - offdata) / (rdata - offdata)
            i = i + 1
        else:
            pass
        continue
    
    x_list = Ta_list['BETDEL']/3600.
    y_list = Ta_list['LAMDEL']/3600.
    x = x_list[0]
    y = y_list[0]
    
    for i in x_list:
        if i != x: dx = i - x; break
        else:pass
    
    for j in y_list:
        if j != y: dy = j - y; break
        else:pass
    
    xgrid = dx
    ygrid = dy
    
    si = len(Ta_list)
    dec = Ta_list['CRVAL3']+Ta_list['BETDEL']/3600.
    
    if Ta_list[0]['OTADEL'].count('N') == 1:
        ind = range(len(Ta_list['OTADEL']))
        count = len(Ta_list['OTADEL'].count('N'))
        nind = -1
        ncount = 0
        pass
    else:
        ind = -1
        count = 0
        nind = range(len(Ta_list['OTADEL']))
        ncount = len(Ta_list['OTADEL'].count('N'))
        pass
    
    ra = Ta_list['OTADEL'].count('N')
    dra = Ta_list['OTADEL'].count('N')
    
    if count != 0:
        ra = Ta_list['CRVAL2'][ind] + Ta_list['LAMDEL'][ind]/3600.
        pass
    elif ncount != 0:
        #ra = Ta_list['CRVAL2'][nind] + Ta_list['LAMDEL'][nind]/3600.
        ra = Ta_list['CRVAL2'][nind] + Ta_list['LAMDEL'][nind]/3600./numpy.cos(dec[nind]*numpy.pi/180.)
        pass
    else:
        pass
    
    ddec = dec - Ta_list[3]['CRVAL3']
    if count != 0:
        dra = ra[ind] - Ta_list[3]['CRVAL2']
        pass
    elif ncount != 0:
        #dra = ra[nind] - Ta_list[3]['CRVAL2']
        dra = (ra[nind] - Ta_list[0]['CRVAL2']) * numpy.cos(dec[nind]*numpy.pi/180.)
        pass
    
    xmin = min(dra)
    xmax = max(dra)
    ymin = min(ddec)
    ymax = max(ddec)
    
    nx = int(round((xmax-xmin)/xgrid))+1
    ny = int(round((ymax-ymin)/ygrid))+1
    nz = len(Ta_list[0]['DATA'])
    
    xind = range(len(dra))
    yind = range(len(ddec))
    for i in range(len(dra)):
        xind[i] = round((xmax - dra[i])/xgrid)
        continue
    
    for j in range(len(ddec)):
        yind[j] = round((ddec[j] - ymin)/ygrid)
        continue
    
    for i in range(len(dra)):
        xind[i] = int(xind[i])
        continue
    
    for j in range(len(ddec)):
        yind[j] = int(yind[j])
        continue
    
    xindsa = (xmax - dra)/xgrid - xind
    yindsa = (ddec - ymin)/ygrid - yind
    
    v = (range(len(Ta_list[0]['DATA']))-Ta_list[0]['CRPIX1']+1)*Ta_list[0]['CDELT1']+Ta_list[0]['CRVAL1']
    buf = range(len(Ta_list[0]['DATA']))
    chrange = [0]*2
    
    chmax = buf[0]
    chmin = buf[len(Ta_list[0]['DATA'])-1]
    vmax = v[0]
    vmin = v[len(Ta_list[0]['DATA'])-1]
    
    chrange[0] = chmax
    chrange[1] = chmin
    
    cube = numpy.zeros([nx,ny,chrange[1]-chrange[0]+1])
    
    for i in range(si): cube[xind[i]][yind[i]] = Ta_list[i]['DATA']
    
    
    timestamp = datetime.datetime.strptime(hdu.data['DATE-OBS'][0], '%Y-%m-%dT%H:%M:%S')
    
    if hdu.data['COORDSYS'][2].lower()=='b1950':
        ctype1 = 'RA---CAR'
        ctype2 = 'DEC--CAR'
        cunit1 = 'deg'
        cunit2 = 'deg'
        equinox = 1950
    elif hdu.data['COORDSYS'][2].lower()=='j2000':
        ctype1 = 'RA---CAR'
        ctype2 = 'DEC--CAR'
        cunit1 = 'deg'
        cunit2 = 'deg'
        equinox = 2000
    elif hdu.data['COORDSYS'][2].lower()=='galactic':
        ctype1 = 'GLON-CAR'
        ctype2 = 'GLAT-CAR'
        cunit1 = 'deg'
        cunit2 = 'deg'
        equinox = 2000
    
    fits_cube = pyfits.PrimaryHDU()
    h = fits_cube.header
    h.update('SIMPLE', 'T')
    h.update('BITPIX', -32)
    h.update('NAXIS', 3)
    h.update('NAXIS1', nx)
    h.update('NAXIS2', ny)
    h.update('NAXIS3', nz)
    h.update('DATE', timestamp.strftime('%Y-%m-%d'))
    h.update('BUNIT','K')
    h.update('CTYPE1', ctype1)
    h.update('CUNIT1', cunit1)
    h.update('CRVAL1',hdu.data['CRVAL2'][2])
    h.update('CRPIX1',xmax/xgrid + 1)
    h.update('CDELT1',-xgrid)
    h.update('CTYPE2', ctype2)
    h.update('CUNIT2', cunit2)
    h.update('CRVAL2',0.0)
    h.update('CRPIX2',-(hdu.data['CRVAL3'][2]+ymin)/ygrid + 1)
    h.update('CDELT2',ygrid)
    h.update('CTYPE3','VELO-LSR')
    h.update('CUNIT3','m/s')
    h.update('CRVAL3',hdu.data['CRVAL1'][0]*1000.)
    h.update('CRPIX3',hdu.data['CRPIX1'][0]-chrange[0])
    h.update('CDELT3',hdu.data['CDELT1'][0]*1000.)
    h.update('EQUINOX', equinox)
    h.update('_OBSERVE', hdu.data['OBSERVER'][0])
    h.update('_OBJECT', hdu.data['OBJECT'][0])
    h.update('_OBS-MOD', hdu.data['OBSMODE'][0])
    h.update('_OBS-DAT', hdu.data['DATE-OBS'][0])
    h.update('_OBS-EXP', hdu.data['EXPOSURE'][2])
    h.update('_OBS-AZ', hdu.data['AZIMUTH'][0])
    h.update('_OBS-EL', hdu.data['ELEVATIO'][0])
    h.update('_OFF-COO', hdu.data['COORDSYS'][off_indices[0]])
    h.update('_OFF-X', hdu.data['CRVAL2'][off_indices[0]])
    h.update('_OFF-Y', hdu.data['CRVAL3'][off_indices[0]])
    h.add_history('created by pyanalyse %s'%analyse.__version__)
    h.add_history('pyanalyse.makespec: generate Ta* data set (mode:OTF)')
    h.add_history('pyanalyse.makespec: time stamp (%s)'%time.strftime('%Y/%m/%d %H:%M:%S'))
    fits_cube.data = cube.T.reshape(nz, ny, nx)
    fits_cube_list = fits_cube
    
    return fits_cube_list

