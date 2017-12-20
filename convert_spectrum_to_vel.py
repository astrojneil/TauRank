import yt
import trident
import h5py
import matplotlib.pyplot as plt
import numpy as np
c = 3e5  #km/s

sightline = 'cloud/pnd_wind'
ion = 'OVI1037'
rest_wave = 1037.0
buf = 150

runList = []
##### Runs to have spectra generated #######
run1 = { 'Name':'T0.3_v1000_chi300_cond',
            'Mach':3.8,
            'tcc':1.7,
            'f_list':['0013', '0038', '0080', '0132']}
run2 = { 'Name':'T0.3_v1700_chi300_cond',
            'Mach':6.5,
            'tcc':1.0,
            'f_list':['0003', '0020', '0046', '0078']}
run3 = { 'Name':'T0.3_v3000_chi300_cond',
            'Mach':11.4,
            'tcc':0.56,
            'f_list':['0001', '0004', '0014', '0035']}
run4 = { 'Name':'T3_v3000_chi3000_cond',
            'Mach':3.6,
            'tcc':1.8,
            'f_list':['0001', '0004', '0007', '0010']}
run6 = { 'Name':'T3_v860_chi3000_cond',
            'Mach':1.0,
            'tcc':6.2,
            'f_list':['0001', '0003', '0006', '0010']}
run7 = { 'Name':'T1_v1700_chi1000_cond',
            'Mach':3.5,
            'tcc':1.8,
            'f_list':['0002', '0010', '0017', '0028']}
run9 = { 'Name':'T10_v1500_chi10000_cond',
            'Mach':1.0,
            'tcc':6.5,
            'f_list':['0001', '0002', '0004', '0008']}
run10 = { 'Name':'T1_v480_chi1000_cond',
            'Mach':1.0,
            'tcc':6.4,
            'f_list':['0002', '0009', '0017', '0031']}
#add the runs to the list that will have spectra generated
runList.append(run1)
runList.append(run2)
runList.append(run3)
runList.append(run4)
runList.append(run6)
runList.append(run7)
runList.append(run9)
runList.append(run10)



#function to read in spectrum, convert to velocity and return
#wavelength and flux numpy arrays
def convert_to_vel(filename, rest_wave, includeWave):
    #load spectrum; will need to add a case when this is a txt file rather than h5
    if(filename[-3:]==".h5"):
        f = h5py.File(filename)
        wavelength = f["wavelength"][:]
        flux = f['flux'][:]
        tau = f['tau'][:]
        f.close()
    else:
        wavelength = []
        flux = []
        f = open(filename, 'r')
        for line in f:
            splitline = line.split(', ')
            wavelength.append(float(splitline[0]))
            flux.append(float(splitline[1]))


    wavelength = np.array(wavelength)
    flux = np.array(flux)
    vel = c*(wavelength/rest_wave -1)

    if includeWave:
        return vel, flux, tau, wavelength
    else:
        return vel, flux, tau

#function to save velocity spectrum
def save_vel_spec(vel, flux, tau, specName):
    saveFile = h5py.File(specName+".h5", "w")
    length = len(vel)
    dset_vel = saveFile.create_dataset("wavelength", (length,), dtype = 'f')
    dset_flux = saveFile.create_dataset("flux", (length,), dtype = 'f')
    dset_tau = saveFile.create_dataset("tau", (length,), dtype = 'f')

    dset_flux[...] = flux
    dset_vel[...] = vel
    dset_tau[...] = tau
    saveFile.close()

    print('Saved Spectrum as '+specName+'.h5')

#function to plot the velocity spectrum
def plot_vel_spectrum(filename, rest_wave, ion, run):
    #buf = input("Range: ")
    vel, flux, tau, wavelength = convert_to_vel(filename, rest_wave, True)

    temp = np.where(wavelength > rest_wave-0.01)
    center = np.where(wavelength[temp] < rest_wave+0.01)
    up_bound = temp[0][center][0]+buf
    low_bound = temp[0][center][0]-buf

    plt.plot(vel[low_bound:up_bound], flux[low_bound:up_bound])
    plt.ylabel('Relative Flux')
    plt.xlabel('Velocity (km/s)')
    plt.title('Mach # = '+str(run['Mach']))

    fig = plt.gcf()
    fig.savefig('../Spectra/CombinedSpec/'+sightline+'/'+ion+'/velSpec'+ion+'_'+run['Name']+'.png')
    fig.clf()
    print('Saved Spectrum figure as velSpec'+ion+'_'+run['Name']+'.png')


def main():
    for run in runList:
        #get info for conversion:
        filename = '../Spectra/CombinedSpec/'+sightline+'/combineSpec_'+run['Name']+'.h5'
        #filename = 'spec/cloud/pnd_wind/spec_raw0035.h5
        vel, flux, tau = convert_to_vel(filename, rest_wave, False)
        save_vel_spec(vel, flux, tau, '../Spectra/CombinedSpec/'+sightline+'/'+ion+'/specVel_'+ion+run['Name'])
        plot_vel_spectrum(filename, rest_wave, ion, run)

if __name__ =="__main__":
    main()
