import yt
import numpy as np
import trident as tri

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")


for i in [6,9,12,13,14,18,21,24,27,35]:
        if i >=1000:
                data = yt.load('KH_hdf5_chk_'+str(i))
        elif i >= 100:
                data = yt.load('KH_hdf5_chk_0'+str(i))
        elif i >= 10:
                data = yt.load('KH_hdf5_chk_00'+str(i))
        else:
                data = yt.load('KH_hdf5_chk_000'+str(i))

        data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

        #try adding an ion field to the dataset
        tri.add_ion_fields(data, ions=['Ne VIII'])
        folder = 'NeVIII'
        #plot the newly added field's number density
        plot = yt.SlicePlot(data, 'z', 'Ne_p7_number_density', origin = 'native')
        plot.set_zlim('Ne_p7_number_density', 1e-16, 5e-6)
        plot.set_cmap("Ne_p7_number_density","gist_rainbow")
        plot.save(folder)
        print('Saved plot as '+folder+'KH_......')

        #plot = yt.SlicePlot(data, 'z', 'velocity_y', origin='native')
        #plot.save()
