import yt
import numpy as np
import trident as tri
import matplotlib.pyplot as plt

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")

#add velocity b parameter field
def _vel_squared(field, data):
    return data['velocity_y']**2

def _b_param(field, data):
    reg = data.ds.all_data()
    vel_Proj = reg.mean('velocity_y', 'y', weight = fieldname)
    vel2_proj = reg.mean('vel_squared', 'y', weight = fieldname)

    bparam = np.sqrt(vel2_proj['vel_squared']- vel_Proj['velocity_y']**2)
    #print(vel_Proj['y'])
    #v = data['ones']
    #bparam.plot()

    #plt.scatter(reg['x'], reg['y'])
    #fig = plt.gcf()
    #fig.savefig('test.png')
    #v[:, 0.0, :]*bparam
    return data.apply_units(bparam, 'cm/s')

######## CHANGE THESE #######
ProjectionFolder = 'Projections_Uneg2'
#ion = 'O VI'
#fieldname = 'O_p5_number_density'
#ionfolder = '/OVI/'
########



def makeProjections(directory, runName, f_list, savefolder, ion, fieldname):
    for i in f_list:
        data = yt.load(directory+runName+'/KH_hdf5_chk_'+i)
        data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')
        #add an ion field to the dataset
        tri.add_ion_fields(data, ions=[ion])

        #add new fields for projection plots
        #data.add_field(('gas', 'vel_squared'), function=_vel_squared, display_name = 'vel squared', units = 'cm**2/s**2')
        #data.add_field(('gas', 'b_param'), function=_b_param, display_name = 'b parameter', units = 'cm/s')

        #plot the the column density
        plot1 = yt.ProjectionPlot(data, 'z', fieldname, origin = 'native')
        plot1.set_zlim(fieldname, 1e8, 1e18)
        plot1.set_cmap(fieldname,"gist_rainbow")
        plot1.save(savefolder)

        #plot the average y-velocity
        #plot2 = yt.ProjectionPlot(data, 'y', 'velocity_y', origin = 'native', weight_field = fieldname)
        #plot2.set_log('velocity_y', False)
        #plot2.set_zlim(fieldname, 1e-16, 5e-6)
        #plot2.set_cmap(fieldname,"gist_rainbow")
        #plot2.save(savefolder)

        #reg = data.all_data()
        #vel_Proj = reg.mean('velocity_y', 'y', weight = fieldname)
        #vel2_proj = reg.mean('vel_squared', 'y', weight = fieldname)

        #bparam = np.sqrt(vel2_proj['vel_squared']- vel_Proj['velocity_y']**2)

        #plt.scatter(vel_Proj['z'], vel_Proj['x'], c=bparam, marker = 'o')
        #plt.contour(vel_Proj['z'], vel_Proj['x'], bparam)
        #plt.colorbar()
        #fig = plt.gcf()
        #fig.savefig('test.png')

        #plot3 = yt.ProjectionPlot(vel_Proj, 'y', 'test', origin = 'native')
        #plot3.set_log('b_param', False)
        #plot3.set_zlim(fieldname, 1e-16, 5e-6)
        #plot3.set_cmap(fieldname,"gist_rainbow")
        #plot3.save(savefolder)


        print('Saved plots as '+savefolder+'KH_......')

    print("Finished with run "+runName)


def runthroughRuns(ion, fieldname, ionfolder, runList):
    for run in runList:
        savefolder = '../'+ProjectionFolder+'/'+run['Name']+ionfolder
        makeProjections(run['Dir'], run['Name'], run['f_list'], savefolder, ion, fieldname)

    print("Finished with Ion"+ion)


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
ionList.append(ion1)
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
