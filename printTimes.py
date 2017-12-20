import yt
import numpy as np

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


outfile = file('runTimes.txt', 'w')
for run in runList:
    outfile.write(run['Name']+', Mach #='+str(run['Mach'])+' Myr \n')
    for chk in run['f_list']:
        data = yt.load('../Files/'+run['Name']+'/KH_hdf5_chk_'+chk)
        timeMyrs = data.current_time.in_units('Myr')
        outfile.write(chk+',\t'+str(timeMyrs)+' \t'+str(timeMyrs/run['tcc'])+' tcc\n')
    outfile.write('\n')
