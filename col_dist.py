import numpy as np
import matplotlib.pyplot as plt
import yt
import trident as tri
ProjectionFolder = 'Projections_Uneg2'

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")


def makeColDist(directory, runName, f_list, savefolder, ion, fieldname):
    for i in f_list:
        data = yt.load(directory+runName+'/KH_hdf5_chk_'+i)
        data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

        #add an ion field to the dataset
        tri.add_ion_fields(data, ions=[ion])

        #projection of the number density
        p = data.proj(fieldname, 1)
        #make fixed resolution buffer (same as when a figure is made)
        #to have an array with every value in each pixel
        frb = yt.FixedResolutionBuffer(p, (-2.464e21, 2.464e21, -2.464e21, 2.464e21), (800, 800))
        #flatten the frb to a 1d array
        flattened_coldens = frb[fieldname].flatten()

        if min(flattened_coldens)==0:
            mincol = 8
        else:
            mincol = np.log10(min(flattened_coldens))
        maxcol = np.log10(max(flattened_coldens))

        #make histogram!
        plt.hist(flattened_coldens, bins = np.logspace(mincol-1, maxcol+1, 50), fill=False, color = 'blue', log=True)
        plt.xscale('log')
        #plt.yscale('log')
        plt.ylabel('Number of pixels')
        plt.xlabel(ion+' Column Density per pixel')
        plt.ylim(1, 1e6)

        fig = plt.gcf()
        fig.savefig(savefolder+'/'+runName+'_'+i+'_'+fieldname+'.png')
        plt.close()


def runthroughRuns(ion, fieldname, ionfolder, runList):
    for run in runList:
        #savefolder='test_colDensDist'
        savefolder = '../'+ProjectionFolder+'/'+run['Name']+ionfolder
        makeColDist(run['Dir'], run['Name'], run['f_list'], savefolder, ion, fieldname)
        print("Finished with Run "+run['Name']+", Ion "+ion)


##### Runs to have spectra generated #######
run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'f_list':['0013', '0038', '0080', '0132']}
run2 = { 'Name':'T3_v3000_chi3000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':3.6,
        'tcc':1.8,
        'f_list':['0001', '0004', '0007', '0010']}
run3 = { 'Name':'T1_v1700_chi1000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':3.5,
        'tcc':1.8,
        'f_list':['0002', '0010', '0017', '0028']}
run4 = { 'Name':'T0.3_v1000_chi300',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':3.8,
        'f_list':['0025', '0033', '0042', '0058']}
run5 = { 'Name':'T3_v3000_chi3000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':3.6,
        'f_list':['0021', '0030', '0040', '0062']}
run6 = { 'Name':'T1_v1700_chi1000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':3.5,
        'f_list':['0021', '0029', '0038', '0052']}
run7 = { 'Name':'HC_v1000_chi300_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0054', '0060', '0080', '0107']}
run8 = { 'Name':'HC_v1700_chi1000_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0024', '0050', '0082', '0083']}
run9 = { 'Name':'HC_v3000_chi3000_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0007', '0015', '0026', '0049']}
run10 = { 'Name':'LowCond_v1700_chi300_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0016', '0075', '0115', '0184']}

run11 = { 'Name':'T0.3_v1700_chi300_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'f_list':['0003', '0020', '0046', '0078']}
run12 = { 'Name':'T0.3_v3000_chi300_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':11.4,
        'tcc':0.56,
        'f_list':['0001', '0004', '0014', '0035']}
run13 = { 'Name':'T3_v860_chi3000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':1.0,
        'tcc':6.2,
        'f_list':['0001', '0003', '0006', '0010']}
run14 = { 'Name':'T10_v1500_chi10000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':1.0,
        'tcc':6.5,
        'f_list':['0001', '0002', '0004', '0008']}
run15 = { 'Name':'T1_v480_chi1000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':1.0,
        'tcc':6.4,
        'f_list':['0002', '0009', '0017', '0031']}

run16 = { 'Name':'T0.3_v1700_chi300',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':6.5,
        'f_list':['0022', '0032', '0053', '0085']}
run17 = { 'Name':'T0.3_v3000_chi300',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':11.4,
        'f_list':['0028', '0044', '0065', '0110']}
run18 = { 'Name':'T3_v430_chi3000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':0.5,
        'f_list':['0010', '0011', '0016', '0024']}
run19 = { 'Name':'T3_v860_chi3000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':1.0,
        'f_list':['0010', '0018', '0030', '0038']}
run20 = { 'Name':'T1_v3000_chi1000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':6.2,
        'f_list':['0022', '0032', '0048', '0095']}
run21 = { 'Name':'T10_v1500_chi10000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':1.0,
        'f_list':['0014', '0021', '0029', '0044']}
run22 = { 'Name':'T1_v480_chi1000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':1.0,
        'f_list':['0009', '0013', '0024', '0035']}


#add the runs to the list that will have spectra generated
runList = []
runList.append(run1)
runList.append(run2)
runList.append(run3)
runList.append(run4)
runList.append(run5)
runList.append(run6)
runList.append(run7)
runList.append(run8)
runList.append(run9)
runList.append(run10)
runList.append(run11)
runList.append(run12)
runList.append(run13)
runList.append(run14)
runList.append(run15)
runList.append(run16)
runList.append(run17)
runList.append(run18)
runList.append(run19)
runList.append(run20)
runList.append(run21)
runList.append(run22)


### dictionaries of ion info
ion1 = {'ion':'O VI',
        'fieldname':'O_p5_number_density',
        'ionfolder': '/OVI/'}
ion2 = {'ion':'Mg II',
        'fieldname':'Mg_p1_number_density',
        'ionfolder': '/MgII/'}
ion3 = {'ion':'N V',
        'fieldname':'N_p4_number_density',
        'ionfolder': '/NV/'}
ion4 = {'ion':'C IV',
        'fieldname':'C_p3_number_density',
        'ionfolder': '/CIV/'}
ion5 = {'ion':'Si III',
        'fieldname':'Si_p2_number_density',
        'ionfolder': '/SiIII/'}
ion6 = {'ion':'Si IV',
        'fieldname':'Si_p3_number_density',
        'ionfolder': '/SiIV/'}
ion7 = {'ion':'Ne VII',
        'fieldname':'Ne_p6_number_density',
        'ionfolder': '/NeVII/'}
ion8 = {'ion':'H I',
        'fieldname':'H_p0_number_density',
        'ionfolder': '/HI/'}
ion9 = {'ion':'C II',
        'fieldname':'C_p1_number_density',
        'ionfolder': '/CII/'}
ion10 = {'ion':'C III',
        'fieldname':'C_p2_number_density',
        'ionfolder': '/CIII/'}


ionList = []
#ionList.append(ion1)
ionList.append(ion2)
ionList.append(ion3)
ionList.append(ion4)
ionList.append(ion5)
ionList.append(ion6)
ionList.append(ion7)
ionList.append(ion8)
ionList.append(ion9)
ionList.append(ion10)


for ion in ionList:
    runthroughRuns(ion['ion'], ion['fieldname'], ion['ionfolder'], runList)
    print("Finished with all Runs for ion "+ion['ion'])
