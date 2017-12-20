import yt
import trident
import h5py
import matplotlib.pyplot as plt
import numpy as np
from convert_spectrum_to_vel import save_vel_spec
### CHANGE THESE ###
sightline = 'cloud/pnd_wind'
######


line_features = {'Ne VIII ab': 770, 'C IV ab': 1550,
            'Mg II ab': 1240, 'O IV abc': 554, 'O IV de': 609,
            'O IV f': 629, 'O IV gh': 790, 'O VI ab': 1031}


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


def makeCombinedSpec(run, specList):
    TotalFlux = np.ones(110001)
    taus = np.zeros(110001)
    for i in specList:
        f = h5py.File('../Spectra/'+run+'/'+sightline+'/spec_raw'+i+'.h5')
        wavelength = f["wavelength"][:]
        flux = f['flux'][:]
        tau = f['tau'][:]
        f.close()

        wavelength = np.array(wavelength)
        flux = np.array(flux)
        tau = np.array(tau)

        TotalFlux = TotalFlux*flux
        taus = taus+tau

    save_vel_spec(wavelength, TotalFlux, taus, '../Spectra/CombinedSpec/'+sightline+'/combineSpec_'+run)

    trident.plot_spectrum(wavelength, TotalFlux, filename = '../Spectra/CombinedSpec/'+sightline+'/combineSpec_'+run+'.png', features = line_features)

    print('Saved Spectrum figure as ../Spectra/CombinedSpec/'+sightline+'/combineSpec_'+run+'.png')

for run in runList:
    makeCombinedSpec(run['Name'], run['f_list'])
