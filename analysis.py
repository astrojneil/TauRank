import numpy as np
import matplotlib.pyplot as plt

run3 = { 'Name':'T1_v1700_chi1000_cond',
    'Dir':'../../Blob_paper2/Files/',
    'Mach':3.5,
    'tcc':1.8,
    'f_list':['0002', '0010', '0017', '0028']}
run6 = { 'Name':'T1_v1700_chi1000',
    'Dir':'../../Blob_paper1/Files/',
    'Mach':3.5,
    'f_list':['0021', '0029', '0038', '0052']}


### dictionaries of ion info
ion1 = {'ion':'O VI',
            'fieldname':'O_p5_number_density',
            'ionfolder': '/OVI/',
            'color': 'brown'}
ion2 = {'ion':'Mg II',
            'fieldname':'Mg_p1_number_density',
            'ionfolder': '/MgII/',
            'color': 'green'}
ion3 = {'ion':'N V',
            'fieldname':'N_p4_number_density',
            'ionfolder': '/NV/',
            'color': 'red'}
ion4 = {'ion':'C IV',
            'fieldname':'C_p3_number_density',
            'ionfolder': '/CIV/',
            'color': 'orange'}
ion5 = {'ion':'Si III',
            'fieldname':'Si_p2_number_density',
            'ionfolder': '/SiIII/',
            'color': 'cyan'}
ion6 = {'ion':'Si IV',
            'fieldname':'Si_p3_number_density',
            'ionfolder': '/SiIV/',
            'color': 'blue'}
ion7 = {'ion':'Ne VII',
            'fieldname':'Ne_p6_number_density',
            'ionfolder': '/NeVII/',
            'color':'pink'}
ion8 = {'ion':'H I',
            'fieldname':'H_p0_number_density',
            'ionfolder': '/HI/',
            'color':'gray'}
ion9 = {'ion':'C II',
            'fieldname':'C_p1_number_density',
            'ionfolder': '/CII/',
            'color':'purple'}
ion10 = {'ion':'C III',
            'fieldname':'C_p2_number_density',
            'ionfolder': '/CIII/',
            'color': 'magenta'}


ionList = []
ionList.append(ion1)
ionList.append(ion2)
ionList.append(ion3)
#ionList.append(ion4)
ionList.append(ion5)
#ionList.append(ion6)
ionList.append(ion7)
#ionList.append(ion8)
ionList.append(ion9)
#ionList.append(ion10)

def readbestTauB(ion, runName):
    openfile = open('../rankTau'+ion['ionfolder']+ion['ionfolder'][1:-1]+'_bestFitParameters.txt', 'r')
    Taus = []
    bs = []
    for line in openfile:
        splitLine = line.split(', ')
        if splitLine[0] == runName:
            Taus.append(float(splitLine[2]))
            bs.append(float(splitLine[5]))

    return Taus, bs

#define functions for the emcee best fit
def model(t, b, x):
    return t*(0.01)/(1.01-x**b)


for ion in ionList:
    taus, bs = readbestTauB(ion, run3['Name'])
    x = np.linspace(0, 1, 7880)
    profile = model(taus[0], bs[0], x)
    plt.plot(x, profile, label = ion['ion'], color = ion['color'])
    #plt.scatter(np.log10(taus), np.log10(bs), label=ion['ion'], marker = 'o', color=ion['color'])
    print(ion['ion'], taus[0], bs[0])
plt.legend()
#plt.xscale('log')
#plt.yscale('log')
plt.show()
