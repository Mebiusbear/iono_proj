# radec2altaz.py
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def radec2altaz(t, long, lat, ra, dec):
    d2r = np.pi/180
    r2d = 180/np.pi

    J2000 = datetime(2000,1,1,12)
    d = (t - J2000).total_seconds() / 86400 #day offset

    UT = t.hour + t.minute/60 + t.second/3600
    LST = (100.46 + 0.985647 * d + long + 15*UT + 360) % 360
    ha = (LST - ra + 360) % 360
    
    x = np.cos(ha*d2r) * np.cos(dec*d2r)
    y = np.sin(ha*d2r) * np.cos(dec*d2r)
    z = np.sin(dec*d2r)
    xhor = x*np.cos((90-lat)*d2r) - z*np.sin((90-lat)*d2r)
    yhor = y
    zhor = x*np.sin((90-lat)*d2r) + z*np.cos((90-lat)*d2r)
    az = np.arctan2(yhor, xhor)*r2d + 180
    alt = np.arcsin(zhor)*r2d
    return alt, az

def plot_altaz(az, alt, color, size, alpha=1, marker='o', ax=None):
    """plot altitude/azimuth coordinates"""
    az  = [(i/180)*np.pi for i in az] #convert to radians
    if ax is None:
        fig = plt.figure()
        ax = fig.add_axes([0.1,0.1,0.8,0.8], polar=True)
        ax.set_theta_zero_location('N')
        #ax.set_theta_direction(-1)
        ax.set_ylim(90, 0)
        ax.set_yticks(np.arange(0,91,15))
    #alt = [90-i for i in alt] # should find a better way
    ax.scatter(az, alt, c=color, s=size, alpha=alpha, marker=marker)
    ax.grid(True, alpha=0.7)
    return ax


t = datetime.utcnow()
long = 7.743881661364198
lat = 48.58333719296604

stars = np.genfromtxt('123.csv', delimiter=',')

size = 0.1 + stars[:,0].max() - stars[:,0]

altS = []
azS = []
for i in range(len(stars)):
    alt, az = radec2altaz(t, long, lat, stars[i,1], stars[i,2])
    altS.append(alt)
    azS.append(az)

ax = plot_altaz(azS, altS, 'k', size**1.8)

pol_radec = {'ra':37.954560670189856, 'dec': 89.26410896994187}
pol_alt, pol_az = radec2altaz(t, long, lat, pol_radec['ra'], pol_radec['dec'])
ax = plot_altaz([pol_az], [pol_alt], 'r', 20, ax=ax, marker='*') #polaris

plt.show()