import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner
import scipy

def openRankedFile(filename):
    openfile = open(filename, 'r')
    rankedTaus = []
    for line in openfile:
        rankedTaus.append(float(line))
    openfile.close()
    return np.array(rankedTaus)

taus = openRankedFile('../rankTau/CIII/rankTauT0.3_v3000_chi300_cond_v182.txt')
totalpixel = len(taus)
pixelNum = np.arange(0.0, totalpixel, 1.0)
pixelFrac = pixelNum/totalpixel

clip = 640000-7880  #total-cloudpixels

pixelFrac_new = (pixelNum[clip:]-clip)/len(pixelNum[clip:])
testquad = -.12/(pixelFrac_new**3-1.05)
testexp = np.exp((pixelFrac_new)**6/1.) - 1

#Try to find the best fit
def lnprior(theta, maxtau):
    tau0, b = theta
    if 0.00 < tau0 < maxtau and 0.0 < b < 1.e2:
        return 0.0
    return -np.inf

def lnlike(theta, tau, frac, err):
    tau0, b = theta
    model = tau0*(0.01)/(1.01-frac**b)
    return -0.5*(np.sum((tau - model)**2/err**2))

def lnprob(theta, tau, frac, err, maxtau):
    lp = lnprior(theta, maxtau)
    if np.isfinite(lp):
        return lp + lnlike(theta, tau, frac, err)
    return -np.inf

#set up emcee
ndim, nwalkers = 2, 200
r = np.ones(ndim)
pos = [r + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(taus[clip:], pixelFrac_new, 1e-2, 2*max(taus[clip:])))

print("Running MCMC...")
sampler.run_mcmc(pos, 1000, rstate0=np.random.get_state())
print("Done.")

#analysis
burnin = 50
samples = sampler.chain[:, burnin:, :].reshape((-1, ndim))

#plot!
#corner plot!
fig = corner.corner(samples, labels=['tau0', 'b'])
fig.savefig("test_triangle3.png")

#plot 100 over true
plt.figure()
for tau0, b in samples[np.random.randint(len(samples), size=100)]:
    model = tau0*(0.01)/(1.01-pixelFrac_new**b)
    plt.plot(pixelFrac_new, model, color = 'k', alpha = 0.2)
plt.scatter(pixelFrac_new, taus[clip:], color = 'red', marker = '.')
plt.xlabel('Fraction of Initial Cloud Area')
plt.ylabel('Optical Depth')
plt.xlim(0, 1.1)
#plt.ylim(-0.1, 2)


tau0_mcmc, b_mcmc = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), zip(*np.percentile(samples, [16, 50, 84], axis=0)))

#the _mcmc variables are now 3 element tuples with 50% percentile, difference between 84% and 50% and difference between 5% and 16% ('errors')
print(tau0_mcmc, b_mcmc)
plt.plot(pixelFrac_new, tau0_mcmc[0]*(0.01/(1.01-pixelFrac_new**b_mcmc[0])), color= 'green')
#plt.plot(pixelFrac_new, tau0_mcmc[0]*(0.01/(1.01-pixelFrac_new**3)), color= 'green')
plt.savefig('fit-mcmc3.png')


#def moduleFun(x):
#    return tau0_mcmc[0]*(0.01/(1.01-x**b_mcmc[0]))

#model_area = scipy.integrate.quad(moduleFun, 0.0, 1)
#print('model: '+str(model_area))
#data_area = np.trapz(taus[clip:], pixelFrac_new)
#print('data: '+str(data_area))

#plt.plot(pixelFrac_new, taus[clip:], linewidth = '3')
#plt.plot(pixelFrac_new, testquad, color = 'red')
#plt.plot(pixelFrac_new, testexp, color = 'green')
#plt.ylim(-0.1, 2)
#plt.xlim(0, 1.1)
#plt.ylabel('Optical Depth')
#plt.xlabel('Fraction of Inital Cloud Area')

#fig = plt.gcf()
#fig.savefig('test_fit.png')
