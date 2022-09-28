from astropy.wcs import WCS
import numpy as np
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import os

# screen_width_metres = 200e3
# frequency = 1e8
# rate = 1.0/60.0
# num_times = 240
# # num_pix = int(screen_width_metres / pscale)

# num_pix = 1000
# pscale = 200
# fln = "pixel_%d_step_6_scale_%d.npy"%(num_pix,pscale)


# npy_filename = os.path.join("../results/arch_python",fln)
# fits_filename = fln[:-3] + "fits"

# w = WCS(naxis=4)
# w.naxis = 4
# w.wcs.cdelt = [pscale, pscale, 1.0 / rate, 1.0]
# w.wcs.ctype = ['XX', 'YY', 'TIME', 'FREQ']
# w.wcs.crval = [0.0, 0.0, 0.0, frequency]          # Coordinate reference values for each coordinate axis.
# data = numpy.zeros([1, num_times, num_pix, num_pix])
# tec = numpy.load(npy_filename)


# for i in range(num_times):
#     data[:, i, ...] += tec[numpy.newaxis, ...]

# fits.writeto(filename=fits_filename, data=data,
#              header=w.to_header(), overwrite=True)

def write_fits(output_image_filename,args):

    # screen_width_metres = 200e3
    frequency = 1e8
    rate = 1.0/60.0
    num_times = 240
    
    num_pix = args.npixel
    pscale = args.pscale

    fits_filename = output_image_filename[:-3] + "fits"
    tec_data = np.load(output_image_filename)

    w = WCS(naxis=4)
    w.naxis = 4
    w.wcs.cdelt = [pscale, pscale, 1.0 / rate, 1.0]
    w.wcs.ctype = ['XX', 'YY', 'TIME', 'FREQ']
    w.wcs.crval = [0.0, 0.0, 0.0, frequency] 

    data = np.zeros([1, num_times, num_pix, num_pix])

    for i in range(num_times):
        data[:, i, ...] += tec_data[np.newaxis, ...]

    fits.writeto(filename=fits_filename, data=data,
             header=w.to_header(), overwrite=True)