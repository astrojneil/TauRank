#code to make 1D plots for the conduction runs
import yt
import matplotlib.pyplot as plt
import numpy as np
import math
import h5py
k = 1.38e-23 #(m^2 kg)/(s^2 K)
gamma = 1.4 #is assume hydrogen
me = 9.109e-31 #kg
kpc = 3.08e21

field = 'temperature'
vel = 1700.0*(1e5) #cm/s
chi = 300.0

def makeRayplots(runName, file_list, speedString):
    for i in file_list:
        #load data
        filename = '../Files/'+runName+'/KH_hdf5_chk_'+i
        #figname = '../Plots/'+field+'Ray_v1000_0013.png'
        figname = '../Plots/eleSoundSpeed_xRay_v'+speedString+'_'+i+'.png'


        #get the frame velocity
        f = h5py.File(filename, 'r')
        velframe = f['real scalars'][7][1] #cm/s
        f.close()

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
        ax = 0 #cut through y axis = 1; x axis = 0
        ray = data.ortho_ray(ax, (0.1*kpc,0))

        #sort ray with y so it's always in the right order
        srt = np.argsort(ray['x'])

        #plot ray!
        #velocity = (np.array(ray[field][srt])+velframe)/1e5
        #density/pressure = np.log10(np.array(ray[field][srt]))
        #electron sound speed = np.log10(np.sqrt(k*np.array(ray[field][srt])/me)/1e3)
        plt.plot(np.array(ray['x'][srt])/3.08e21, np.log10(np.sqrt(k*np.array(ray[field][srt])/me)/1e3)  )
        #plt.yscale('log')
        plt.xlabel('x (kpc)')
        plt.ylabel('log( Electron sound speed (km/s))')
        plt.ylim(1.7, 4.2)
        plt.annotate('t/tcc = '+str(round(time_tcc.v,2)), xy = (0.45, 2.6))
        plt.annotate('t = '+str(round(timeBig.v,2))+' Myrs', xy = (0.45, 2.5))

        fig = plt.gcf()
        fig.savefig(figname)
        fig.clf()
        print('Saved figure as '+figname)

list_1000 = ['0013', '0038', '0080', '0132']
list_1700 = ['0003', '0020', '0046', '0078']

makeRayplots('T0.3_v1700_chi300_cond', list_1700, '1700')
