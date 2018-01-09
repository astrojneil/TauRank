import numpy as np
import matplotlib.pyplot as plt

##### Runs to have spectra generated #######
run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'f_list':['0013', '0038', '0080', '0132'],
        'marker':'^',
        'color':'#4c95cb'}
run2 = { 'Name':'T0.3_v1700_chi300_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'f_list':['0003', '0020', '0046', '0078'],
        'marker':'^',
        'color':'#0068b6'}
run3 = { 'Name':'T0.3_v3000_chi300_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':11.4,
        'tcc':0.56,
        'f_list':['0001', '0004', '0014', '0035'],
        'marker':'^',
        'color':'#00487f'}
run5 = { 'Name':'T3_v860_chi3000_cond',
            'Dir':'../../Blob_paper2/Files/',
            'Mach':1.0,
            'tcc':6.2,
            'f_list':['0001', '0003', '0006', '0010'],
            'marker':'^',
            'color':'#f0a10b'}
run4 = { 'Name':'T3_v3000_chi3000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':3.6,
        'tcc':1.8,
        'f_list':['0001', '0004', '0007', '0010'],
        'marker':'^',
        'color':'#a87007'}
run7 = { 'Name':'T1_v480_chi1000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':1.0,
        'tcc':6.4,
        'f_list':['0002', '0009', '0017', '0031'],
        'marker':'^',
        'color':'#4ca85c'}
run6 = { 'Name':'T1_v1700_chi1000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':3.5,
        'tcc':1.8,
        'f_list':['0002', '0010', '0017', '0028'],
        'marker':'^',
        'color':'#008317'}
run8 = { 'Name':'T10_v1500_chi10000_cond',
        'Dir':'../../Blob_paper2/Files/',
        'Mach':1.0,
        'tcc':6.5,
        'f_list':['0001', '0002', '0004', '0008'],
        'marker':'^',
        'color':'#a90606'}

run9 = { 'Name':'T0.3_v1000_chi300',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':3.8,
        'f_list':['0025', '0033', '0042', '0058'],
        'marker':'o',
        'color':'#4c95cb'}
run10 = { 'Name':'T0.3_v1700_chi300',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':6.5,
        'f_list':['0022', '0032', '0053', '0085'],
        'marker':'o',
        'color':'#0068b6'}
run11 = { 'Name':'T0.3_v3000_chi300',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':11.4,
        'f_list':['0028', '0044', '0065', '0110'],
        'marker':'o',
        'color':'#00487f'}
run13 = { 'Name':'T3_v430_chi3000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':0.5,
        'f_list':['0010', '0011', '0016', '0024'],
        'marker':'o',
        'color':'#f4bd54'}
run14 = { 'Name':'T3_v860_chi3000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':1.0,
        'f_list':['0010', '0018', '0030', '0038'],
        'marker':'o',
        'color':'#f0a10b'}
run12 = { 'Name':'T3_v3000_chi3000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':3.6,
        'f_list':['0021', '0030', '0040', '0062'],
        'marker':'o',
        'color':'#a87007'}

run17 = { 'Name':'T1_v480_chi1000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':1.0,
        'f_list':['0009', '0013', '0024', '0035'],
        'marker':'o',
        'color':'#4ca85c'}
run15 = { 'Name':'T1_v1700_chi1000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':3.5,
        'f_list':['0021', '0029', '0038', '0052'],
        'marker':'o',
        'color':'#008317'}
run16 = { 'Name':'T1_v3000_chi1000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':6.2,
        'f_list':['0022', '0032', '0048', '0095'],
        'marker':'o',
        'color':'#005b10'}

run18 = { 'Name':'T10_v1500_chi10000',
        'Dir':'../../Blob_paper1/Files/',
        'Mach':1.0,
        'f_list':['0014', '0021', '0029', '0044'],
        'marker':'o',
        'color':'#a90606'}

run19 = { 'Name':'HC_v1000_chi300_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0054', '0060', '0080', '0107'],
        'marker':'s',
        'color':'#ae66bc'}
run20 = { 'Name':'HC_v1700_chi1000_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0024', '0050', '0082', '0083'],
        'marker':'s',
        'color':'#790090'}
run21 = { 'Name':'HC_v3000_chi3000_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0007', '0015', '0026', '0049'],
        'marker':'s',
        'color':'#540064'}
run22 = { 'Name':'LowCond_v1700_chi300_cond',
        'Dir':'../../Blob_paper3/Files/',
        'Mach':3.5,
        'f_list':['0016', '0075', '0115', '0184'],
        'marker':'.',
        'color':'black'}









#add the runs to the list that will have spectra generated
runList = []
runList.append(run1)
runList.append(run2)
runList.append(run3)
runList.append(run5)
runList.append(run4)
runList.append(run7)
runList.append(run6)
runList.append(run8)
runList.append(run9)
runList.append(run10)
runList.append(run11)
runList.append(run13)
runList.append(run14)
runList.append(run12)
runList.append(run17)
runList.append(run15)
runList.append(run16)
runList.append(run18)
runList.append(run19)
runList.append(run20)
runList.append(run21)
runList.append(run22)


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
ionList.append(ion4)
ionList.append(ion5)
ionList.append(ion6)
ionList.append(ion7)
ionList.append(ion8)
ionList.append(ion9)
ionList.append(ion10)

def readbestTauB(ion, runName):
    openfile = open('../rankTau'+ion['ionfolder']+ion['ionfolder'][1:-1]+'_bestFitParameters_3.txt', 'r')
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

#fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)

for ion in ionList:
    fig = plt.figure()
    ax = plt.subplot(111)
    for run in runList:
        taus, bs = readbestTauB(ion, run['Name'])
        x = np.linspace(0, 1, 7880)
        #profile = model(taus[0], bs[0], x)
        #ax.plot(x[0:7800], profile[0:7800], label = ion['ion'], color = ion['color'])
    #for i in range(len(taus)):
    #    if i==0:
    #        j=0
    #        k=0 #top left
    #    if i==1:
    #        j=0
    #        k=1 #top right
    #    if i==2:
    #        j=1 #lower left
    #        k=0
    #    if i==3:
    #        j=1 #lower right
    #        k=1
        ax.scatter(np.log10(taus), np.log10(bs), label=run['Name'], marker = run['marker'], color = run['color'])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
    ax.set_title(ion['ion'])
    ax.set_xlabel('log(tau)')
    ax.set_ylabel('log(b)')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #plt.xscale('log')
    fig.set_size_inches(12, 6)
    #fig.savefig('test.png')
    fig.savefig('../rankTau'+ion['ionfolder']+ion['ionfolder'][1:-1]+'.png')
    fig.savefig('tauBAnalysis_all/'+ion['ionfolder'][1:-1]+'.png')
