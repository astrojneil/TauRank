# Basic script for using Trident (Hummels et al 2016)
# This script opens a dataset, estimates the ionization fraction,
# calculates a ray and generates a synthetic spectra

#import required packages
import yt
import numpy as np
import trident as tri
kpc = 3.08e21

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")

######## CHNAGE THESE - light of sight ##########
title = 'diag '
savefolderEnd = '/cloud/diag/'
#define the edges of ray to go through entire dataset from left to right
#(must be 3 element tuple of coordinates in physical domain in units of cm)
ray_start = (-0.6*kpc, -0.2*kpc, 1.0)
ray_end = (0.6*kpc, 0.6*kpc, 1.0)
########

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


#list which absorbtion lines to include
line_list = ['O IV', 'Ne VIII', 'O VI', 'C IV', 'N V']
line_features = {'Ne VIII ab': 770, 'C IV ab': 1550,
            'N V': 1240, 'O IV abc': 554, 'O IV de': 609,
            'O IV f': 629, 'O IV gh': 790, 'O VI ab': 1031}

#function to calculateSpectra for a given light of sight, for the run specified by the input parameters
def calculateSpectra(runName, savefolder, file_list):
    filePrefix = '../Files/'+runName+'/KH_hdf5_chk_'
    for chk_num in file_list:
        file_name = filePrefix+chk_num

        dataset = yt.load(file_name)

        dataset.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

        #make a ray object
        ray = tri.make_simple_ray(dataset,
                            redshift=0.0,
                            start_position=ray_start,
                            end_position=ray_end,
                            lines=line_list,
                            ftype = 'gas')

                            #plot and save density projection to look at the path of the ray
        p = yt.ProjectionPlot(dataset, 'z', 'density', origin='native')
        p.annotate_ray(ray)
        p.save(savefolder+'projection'+chk_num+'.png')
        print("Saved Projection images as "+savefolder+"/projection"+chk_num+".png")

        #create a spectrumGenerator; you may make your own spectrograph settings
        sg = tri.SpectrumGenerator(lambda_min= 500, lambda_max=1600, dlambda=0.01)  #uses default spectrograph settings for "Cosmic Origins Spectrograph"
        sg.make_spectrum(ray, lines=line_list)

        #save and plot the spectrum
        sg.save_spectrum(savefolder+'spec_raw'+chk_num+'.h5')
        sg.plot_spectrum(savefolder+'spec_raw'+chk_num+'.png',
                        features = line_features, title = title+chk_num, flux_limits = (0,1.5))

        print("Saved Spectrum as "+savefolder+"spec_raw"+chk_num+"_NV.h5")
        print("Saved Spectrum image as "+savefolder+"spec_raw"+chk_num+"_NV.png")

    print("Finished with "+runName)

for run in runList:
    savefolder = '../Spectra/'+run['Name']+savefolderEnd
    calculateSpectra(run['Name'], savefolder, run['f_list'])
