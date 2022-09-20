import numpy
from astropy.io import fits
from astropy.wcs import WCS
from ARatmospy.ArScreens import ArScreens
screen_width_metres = 200e3
r0 = 5e3  # Scale size (5 km).
bmax = 20e3  # 20 km sub-aperture size.
sampling = 100.0  # 100 m/pixel.
m = int(bmax / sampling)  # Pixels per sub-aperture (200).
n = int(screen_width_metres / bmax)  # Sub-apertures across the screen (10).
num_pix = n * m
pscale = screen_width_metres / (n * m)  # Pixel scale (100 m/pixel).
print("Number of pixels %d, pixel size %.3f m" % (num_pix, pscale))
print("Field of view %.1f (m)" % (num_pix * pscale))
speed = 150e3 / 3600.0  # 150 km/h in m/s.
# Parameters for each layer.
# (scale size [m], speed [m/s], direction [deg], layer height [m]).
layer_params = numpy.array([(r0, speed, 60.0, 300e3),
                            (r0, speed/2.0, -30.0, 310e3),
                            (r0, speed/2.0, -15.0, 320e3)])

rate = 1.0/60.0  # The inverse frame rate (1 per minute).
alpha_mag = 0.999  # Evolve screen slowly.
num_times = 240  # Four hours.
my_screens = ArScreens(n, m, pscale, rate, layer_params, alpha_mag)
my_screens.run(num_times)

# Convert to TEC
# phase = image[pixel] * -8.44797245e9 / frequency
frequency = 1e8
phase2tec = -frequency / 8.44797245e9

w = WCS(naxis=4)
w.naxis = 4
w.wcs.cdelt = [pscale, pscale, 1.0 / rate, 1.0]
w.wcs.crpix = [num_pix // 2 + 1, num_pix // 2 + 1, num_times // 2 + 1, 1.0]
w.wcs.ctype = ['XX', 'YY', 'TIME', 'FREQ']
w.wcs.crval = [0.0, 0.0, 0.0, frequency]
data = numpy.zeros([1, num_times, num_pix, num_pix])
for layer in range(len(my_screens.screens)):
    for i, screen in enumerate(my_screens.screens[layer]):
        data[:, i, ...] += phase2tec * screen[numpy.newaxis, ...]
fits.writeto(filename='test_screen_60s.fits', data=data,
             header=w.to_header(), overwrite=True)