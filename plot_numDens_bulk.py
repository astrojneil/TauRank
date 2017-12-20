import yt
import numpy as np
import trident as tri

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")
def _NV_OVI(field, data):
    return data['N_p4_number_density']/data['O_p5_number_density']

######## CHANGE THESE #######
ion = 'Mg II'
fieldname = 'Mg_p1_number_density'
ionfolder = '/NV_OVI/'
########


def makeNumDensPlot(runName, f_list, savefolder):
    for i in f_list:
        data = yt.load('../Files/'+runName+'/KH_hdf5_chk_'+i)

        data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

        #try adding an ion field to the dataset
        tri.add_ion_fields(data, ions=[ion])

        #plot the newly added field's number density
        plot = yt.SlicePlot(data, 'z', fieldname, origin = 'native')
        plot.set_zlim(fieldname, 1e-16, 5e-6)
        plot.set_cmap(fieldname,"gist_rainbow")

        plot.save(savefolder)
        print('Saved plot as '+savefolder+'KH_......')

    print("Finished with run "+runName)

def makeNV_OVIPlot(runName, f_list, savefolder):
    for i in f_list:
        data = yt.load('../Files/'+runName+'/KH_hdf5_chk_'+i)
        data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

        #try adding an ion field to the dataset
        tri.add_ion_fields(data, ions=['N V', 'O VI'])
        data.add_field(('gas', 'NV_OVI'), function=_NV_OVI, display_name="NV / OVI")

        plot = yt.SlicePlot(data, 'z', 'NV_OVI', origin='native')
        plot.set_cmap('NV_OVI', "gist_rainbow")
        plot.save(savefolder+'NV_OVI'+i)



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


for run in runList:
    savefolder = '../NumDens/'+run['Name']+ionfolder
    makeNV_OVIPlot(run['Name'], run['f_list'], savefolder)
    #makeNumDensPlot(run['Name'], run['f_list'], savefolder)
