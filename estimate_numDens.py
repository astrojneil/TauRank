import yt
import trident
import h5py
import matplotlib.pyplot as plt
import numpy as np
from convert_spectrum_to_vel import convert_to_vel, plot_vel_spectrum, save_vel_spec
c = 3e10  #cm/s
me = 9.11e-28 #g
charge = 4.8e-10 #cgs gaussian, 1.6e-20 (EMU)


#approximate the optical depth tau(v) = ln(I_C/I(v))
def find_tau(flux):
    tau = np.log(1/flux)
    return tau

def find_colDens(tau, rest_wave, oscStren):
    const = (me*c)/(np.pi*charge**2)
    denom = oscStren*(rest_wave*1e-8)
    n = const/denom*tau
    return n

#function to plot the velocity spectrum
def plot_colDens_spectrum(filename, rest_wave, oscStren, ion):
    buf = input("Range: ")
    vel, flux, tau, wavelength = convert_to_vel(filename, rest_wave, True)

    n = find_colDens(tau, rest_wave, oscStren)

    temp = np.where(wavelength > rest_wave-0.01)
    center = np.where(wavelength[temp] < rest_wave+0.01)
    up_bound = temp[0][center][0]+buf
    low_bound = temp[0][center][0]-buf

    plt.plot(vel[low_bound:up_bound], n[low_bound:up_bound])
    plt.ylabel('Column Density')
    plt.xlabel('Velocity (km/s)')

    fig = plt.gcf()
    fig.savefig('colSpec'+ion+'.png')
    print('Saved spectrum figure as colSpec'+ion+'.png')



def main():
    filename = raw_input("Spectrum file: ")
    ion = raw_input("Ion: ")
    rest_wave = float(raw_input("Rest wavelength: "))
    oscStren = float(raw_input("Ocsillator strength: "))
    plot_colDens_spectrum(filename, rest_wave, oscStren, ion)



if __name__=="__main__":
    main()
