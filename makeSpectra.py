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



#list which absorbtion lines to include
line_list = ['O IV', 'Ne VIII', 'Mg II', 'O VI', 'C IV', 'Si III']
line_features = {'Ne VIII ab': 770, 'C IV ab': 1550,
            'Mg II ab': 1240, 'O IV abc': 554, 'O IV de': 609,
            'O IV f': 629, 'O IV gh': 790, 'O VI ab': 1031}

######## CHNAGE THESE ##########
runName = 'T0.3_v1000_chi300'
file_list = ['0011', '0017', '0025', '0026', '0033', '0040', '0042', '0058', '0062']
title = 'diag '
savefolderEnd = '/cloud/diag/'
#define the edges of ray to go through entire dataset from left to right
#(must be 3 element tuple of coordinates in physical domain in units of cm)
ray_start = (-0.6*kpc, -0.2*kpc, 1.0)
ray_end = (0.6*kpc, 0.6*kpc, 1.0)
########

savefolder = '../Spectra/'+runName+savefolderEnd
filePrefix = '../Files/'+runName+'/KH_hdf5_chk_'

#cdfile_list = ['0006']
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

    print("Saved Spectrum as "+savefolder+"spec_raw"+chk_num+".h5")
    print("Saved Spectrum image as "+savefolder+"spec_raw"+chk_num+".png")
