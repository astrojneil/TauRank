import yt
import numpy as np
import trident as tri
import matplotlib.pyplot as plt
import subprocess
from yt.data_objects.particle_filters import add_particle_filter
import h5py
from yt.units import centimeter, gram, second, Kelvin, erg

kpc = 3.086e+21*centimeter
c_speed = 3.0e10  #cm/s
mp = 1.6726e-24*gram #grams
kb = 1.3806e-16*erg/Kelvin   #egs/K


#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    v = data['ones']  #sets metallicity to 1 Zsun
    return data.apply_units(v, "Zsun")


def deleteProjections(listofFiles):
    for num in listofFiles:
        subprocess.call("rm KH_hdf5_chk_"+num+"_proj.h5")

######## CHANGE THESE #######
ProjectionFolder = 'Projections_Uneg2'
#ion = 'O VI'
#fieldname = 'O_p5_number_density'
#ionfolder = '/OVI/'
########

#function to determine the velocity of the cloud for a particular run
#will return an array of velocities (km/s) for the appropriate velocity bins to use
#in the observational data.
def findCloudVel(directory, runName, f_list):
    velList = []
    velFrames = []
    for i in f_list:
        data = yt.load(directory+runName+'/KH_hdf5_chk_'+i)
        allDataRegion = data.all_data()
        cloudRegion = allDataRegion.cut_region(['obj["density"] >= 3.33e-25'])  #at or above 1/3 original density (1e-24)
        avg_vy_cloud = cloudRegion.quantities.weighted_average_quantity('vely', 'ones') #vely is the velocity in the radial direction (towards/away obs)

        #need to add the frame velocity!
        #get the frame velocity
        f = h5py.File(directory+runName+'/KH_hdf5_chk_'+i, 'r')
        velframe = f['real scalars'][7][1] #cm/s
        velFrames.append(velframe/1.0e5) #append frame vel in km/s
        f.close()

        vy_cloud = (avg_vy_cloud.value+velframe)/1.0e5  #convert to km/s
        velList.append(vy_cloud)

    print('Frame vels:')
    print(velFrames)
    print('Cloud vels:')
    print(velList)
    return velList, velFrames


def calcIntColDens(directory, runName, runNumber, ions, velocityBin, frameVel):
    #load and add ions to the dataset
    velocityBin = velocityBin*1.0e5  #convert to cm/s
    frameVel = frameVel*1.0e5  #convert to cm/s
    data = yt.load(directory+runName+'/KH_hdf5_chk_'+runNumber)
    data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

    absorbFracs = []
    #add ion fields to the dataset
    for ion in ions:
        tri.add_ion_fields(data, ions=[ion['ion']])

        #define the function for b(x) for this particular ion
        ### function definition in a for loop... Ew... ###
        def _soundSpeed(field, data):
            topFrac = 2.0*kb*data['temperature']
            botFrac = ion['massNum']*mp
            b = np.sqrt(topFrac/botFrac)
            return b

        #add b_soundSpeed to the dataset
        data.add_field(('gas', 'b_soundSpeed'), function=_soundSpeed, display_name="B Sound Speed", units = 'cm/s', force_override=True)

        #define the function for dTau for this particular ion/velocity
        ### function definition in a for loop... Ew... ###
        def _dTau(field, data):
            term1 = data[ion['fieldname']]/data['b_soundSpeed']
            #assumes velocity is now cm/s
            #must add the frame velocity to the y velocity!
            expTerm = (((data['velocity_y']+frameVel*(centimeter/second)) - velocityBin*(centimeter/second))/data['b_soundSpeed'])**2.0
            dtau = term1*np.exp(-1.0*expTerm)
            return dtau

        #add dTau to the dataset
        data.add_field(('gas', 'tau'), function=_dTau, display_name="dTau", units = 's/cm**4', force_override=True)

        #make cylinder, project through the y axis
        reg = data.disk([0.0, 0.2*kpc, 0.0], [0,1,0], (0.25, 'kpc'), (1.6, 'kpc'))
        #reg = data.all_data()

        p = yt.ProjectionPlot(data, 'y', 'tau', data_source=reg)  # 10/18/2017 !!!! Z axis??? shouldn't it be y?!
        #p.set_zlim(fieldname, 4e11, 2e14)
        #p.save()
        projSave = p.data_source.save_as_dataset(fields = ['tau', ion['fieldname']])

        #load projection as a dataset, add absorption field
        test = yt.load(projSave)


        def no_ColumnDepth(pfilter, data):
            colDepth = data[ion['fieldname']]
            filter = np.logical_or(colDepth != 0.0, colDepth > 0.0)
            return filter
        #select circle/sphere and sum up absorption
        testregion = test.all_data()
        #add_particle_filter("no_colDepth", function=no_ColumnDepth, filtered_type='all', requires=[ion['fieldname']])
        #test.add_particle_filter('no_colDepth')
        hasColumnDens = (testregion[ion['fieldname']] != 0.0)



        tau_coef = (c_speed*(centimeter/second)*ion['sigma']*centimeter*centimeter)/np.sqrt(np.pi)
        #print(tau_coef)
        projectedTau = tau_coef*testregion[('all', 'tau')][hasColumnDens]
        averageAbs = np.average(np.exp(-1.0*projectedTau))
        characteristicTau = np.log(averageAbs)


        absorbFracs.append(characteristicTau)


    return absorbFracs


def calcIntVel(directory, runName, runNumber, ions, velocityBin, frameVel):
    #load and add ions to the dataset
    velocityBin = velocityBin*1.0e5  #convert to cm/s
    frameVel = frameVel*1.0e5  #convert to cm/s
    data = yt.load(directory+runName+'/KH_hdf5_chk_'+runNumber)
    data.add_field(('gas', 'metallicity'), function=_metallicity, display_name="Metallicity", units='Zsun')

    #add ion fields to the dataset
    IntVels = []
    for ion in ions:
        tri.add_ion_fields(data, ions=[ion['ion']])

        #make cylinder
        reg = data.disk([0.0, 0.2*kpc, 0.0], [0,1,0], (0.25, 'kpc'), (1.6, 'kpc'))
        #reg = data.all_data()

        #meanVel + frameVel will be the final mean velocity
        meanVel = reg.quantities.weighted_average_quantity("velocity_y", weight_field=ion['fieldname'])
        finalmeanVel = meanVel+frameVel

        IntVels.append(finalmeanVel)

    return IntVels



def runthroughRuns(ion, fieldname, ionfolder, runList):
    for run in runList:
        #savefolder = '../'+ProjectionFolder+'/'+run['Name']+ionfolder
        #calcAbsorb(run['Dir'], run['Name'], run['f_list'], savefolder, ion, fieldname)
        velocities = findCloudVel(run['Dir'], run['Name'], run['f_list'])
        print velocities

    print("Finished with Ion"+ion)

def main():
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
    '''
    run6 = { 'Name':'T1_v1700_chi1000_lref4',
                'Dir':'../../Blob_paper1/Files/',
                'Mach':3.5,
                'f_list':['0020', '0030', '0040', '0050']}
    run7 = { 'Name':'T1_v1700_chi1000_lref6',
                'Dir':'../../Blob_paper1/Files/',
                'Mach':3.5,
                'f_list':['0021', '0029', '0038']}
    '''


### dictionaries of ion info
    ion1 = {'ion':'O VI',
        'fieldname':'O_p5_number_density',
        'ionfolder': '/OVI/',
        'rest_wave': 1031.91,
        'data_file': '../Files/S1226-o6-forJNeil',
        'sigma': 1.1776e-18,
        'massNum': 16.0}
    ion2 = {'ion':'C IV',
        'fieldname':'C_p3_number_density',
        'ionfolder': '/CIV/',
        'rest_wave': 1548.18,
        'data_file': '../Files/S1226-redward-forJNeil',
        'sigma': 2.5347e-18,
        'massNum': 12.0}
    ion3 = {'ion':'N V',
        'fieldname':'N_p4_number_density',
        'ionfolder': '/NV/',
        'rest_wave': 1242.8,
        'data_file': '../Files/S1226-redward-forJNeil',
        'sigma': 8.3181e-18,
        'massNum': 14.0}
    ion4 = {'ion':'C II',
        'fieldname':'C_p1_number_density',
        'ionfolder': '/CII/',
        'rest_wave': 1335.66,
        'data_file': '../Files/S1226-redward-forJNeil',
        'sigma': 1.4555e-19,
        'massNum': 12.0}

    ionList = []
    ionList.append(ion1)
    ionList.append(ion2)
    ionList.append(ion3)
    ionList.append(ion4)



### run though functions!
    for run in runList:
        #open file so save results
        saveData = open('absorptionFits/absorptionFits'+run['Name']+'_y.txt', 'w')
        saveData.write('VelocityBin, c, OVI_flux, CIV_flux, NV_flux, CII_flux\n')
        #find appropriate velocity bins
        velBins, velFrames = findCloudVel(run['Dir'], run['Name'], run['f_list'])  #velocities are in km/s
        #velBins = [116.88]
        for v in range(len(velBins)): #velocity = velBins[v]
            #calculate characteristic tau for each ion
            colDensList = calcIntColDens(run['Dir'], run['Name'], run['f_list'][v], ionList, velBins[v], velFrames[v])


        #delete projection files made - clean up!
        #deleteProjections(run['f_list'])




if __name__ =="__main__":
    main()
