import yt
import math

#input the radius of the cloud!!
cloud_r = 3.08e20

#find cloud crushing time:
data = yt.load('KH_hdf5_chk_0006')
radius = cloud_r*data.length_unit.in_units('cm') #100 pc in cm
ds = data.all_data()
high_rho = ds['density'].max()
low_rho = ds['density'].min()
vel = ds['vely'].max()*data.velocity_unit.in_units('cm/s')
chi = high_rho/low_rho

one_sec = data.quan(1, 's')
tcc = (radius/vel)*math.sqrt(chi)*(data.length_unit.in_units('code_length')/data.time_unit.in_units('code_time')) #in seconds
#tcc = tcc/(3.14e7)/1e6  #in Myrs


#for field in data.derived_field_list:
	#print(field)

#for i in [25]:
for i in [6,9]:
	if i >=1000:
		data = yt.load('KH_hdf5_plt_cnt_'+str(i))
	elif i >= 100:
		data = yt.load('KH_hdf5_plt_cnt_0'+str(i))
	elif i >= 10:
		data = yt.load('KH_hdf5_chk_00'+str(i))
	else:
		data = yt.load('KH_hdf5_chk_000'+str(i))
	
	plot1 = yt.SlicePlot(data, 'z', 'density', origin='native')



	#plot1.set_zlim('magnetic_field_magnitude', 5e-8, 1e-5)

	#plot1.annotate_grids()
	#plot1.annotate_magnetic_field()
	#plot1.annotate_velocity()
	time = data.current_time.in_units('s')
	time_tcc = time/tcc

	plot1.annotate_timestamp()
	plot1.annotate_text([-0.7,-1.0], 't/tcc = '+str(round(time_tcc.v,2)), coord_system = 'plot')
	#plot1.annotate_arrow((-1.492E+20,  1.112E+21, -1.877E+20), length=0.06, plot_args={'color':'blue'})
	#plot1.annotate_arrow((-1.299E+20,  1.102E+21, -1.684E+20), length=0.05, plot_args={'color':'red'})
	plot1.save('dens'+str(i))
