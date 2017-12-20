#code to make 1D plots for the conduction runs
import yt
import matplotlib.pyplot as plt
import numpy as np
import math
k = 1.38e-23 #(m^2 kg)/(s^2 K)
gamma = 1.4 #is assume hydrogen
me = 9.109e-31 #kg

#load data
filename = '../Files/T0.3_v1700_chi300_cond/KH_hdf5_chk_0020'
field = 'temperature'
#figname = '../Plots/'+field+'Ray_v1000_0013.png'
figname = '../Plots/travelTimeRay_v1700_0020.png'
vel = 1700.0*(1e5) #cm/s
chi = 300.0
data = yt.load(filename)

#load time, calculate cloud crushing time
time = data.current_time.in_units('s')
timeBig = data.current_time.in_units('Myr')
#input the radius of the cloud!!
cloud_r = 3.08e20
#find cloud crushing time:
radius = cloud_r*data.length_unit.in_units('cm') #100 pc in cm
#one_sec = data.quan(1, 's')
tcc = (radius/vel)*math.sqrt(chi)*(data.length_unit.in_units('code_length')/data.time_unit.in_units('code_time')) #in seconds
time_tcc = time/tcc

#select ray along y axis centered at x=0 and z=0
ax = 1 #cut through y axis
ray = data.ortho_ray(ax, (0,0))

#sort ray with y so it's always in the right order
srt = np.argsort(ray['y'])

#plot ray!
plt.plot(np.array(ray['y'][srt])/3.08e21, (cloud_r/1e3)/np.sqrt(k*np.array(ray[field][srt])/me)   )
plt.yscale('log')
plt.xlabel('y (kpc)')
plt.ylabel('Electron Travel Time to Center of Cloud (s)')
#plt.ylim(3, 7)
#plt.annotate('t/tcc = '+str(round(time_tcc.v,2)), xy = (0.5, 2.0))
#plt.annotate('t = '+str(round(timeBig.v,2))+' Myrs', xy = (0.5, 1.9))

fig = plt.gcf()
fig.savefig(figname)
print('Saved figure as '+figname)
