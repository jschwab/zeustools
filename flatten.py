import helmholtz
import numpy as np
from scipy.interpolate import interp1d

# this module provides the ability to average a zeus run along a specified axis

# define generic container to hold the averaged results

class OneD:

    def __init__(self):
        pass

    def write(self, filename):
               # collist = ("r","menc","d","e","T","s",
               #            "j","omega","zbar","abar","aspect"):    
        cols = (self.r, self.menc, 
                self.d, self.e, self.T, self.s, 
                self.j, self.omega, self.abar, self.zbar, 
                self.aspect)

        np.savetxt("{}.1D".format(filename), 
                   np.transpose(cols), fmt = '%10.3E ')

        if hasattr(self,'X'):
            np.savetxt("{}.1DX".format(filename), 
                       np.transpose(self.X), fmt = '%10.3E ')


# define average functions

def weightedavg_2d(field, weight, slice):
    return (np.sum(field[slice,:] * weight[slice,:], axis = 0) / 
            np.sum(weight[slice,:], axis = 0))

def Xweightedavg_2d(field, weight):
    return (np.sum(field * weight,  axis = 1) / 
            np.sum(weight, axis = 0))

def weightedavg_3d(field, weight):
    return (np.sum(np.sum(field * weight, axis = 0),axis = 0) / 
            np.sum(np.sum(weight, axis = 0),axis = 0))

def Xweightedavg_3d(field, weight):
    return (np.sum(np.sum(field * weight,  axis = 1),axis=1) / 
            np.sum(np.sum(weight, axis = 0), axis = 0))


def twod_to_oned(data):

    sdata = OneD()

    # spherical radius
    sdata.N = data.x1.size
    sdata.r = data.x1

    # cylindrical radius
    RR = np.outer(np.sin(data.x2), data.x1)

    # volume & mass weights
    dV = data.dV1[None,:] * data.dV2[:,None] * data.dV3
    dm = data.d * dV

    # define equatorial and polar slices
    polar, = np.where(data.x2 < np.pi / 8.0)
    equatorial, = np.where(data.x2 > 3.0 * np.pi / 8.0)
    full, = np.where(data.x2 != -1)

    # enclosed mass (spherical)
    dmr = np.sum(dm, axis = 0)
    if max(data.x2) < 2:
        msun = 2.0e33 * 0.5 #(fudge)
    else:
        msun = 2.0e33

    sdata.menc = np.cumsum(dmr) / msun

    dj = dm * data.v3 * RR

    # internal energy & density
    sdata.e = weightedavg_2d(data.e, dV, full)
    sdata.d = weightedavg_2d(data.d, dV, full)

    # calculate abar & zbar
    if data.X is not None: 

        sdata.X = Xweightedavg_2d(data.X, dm)

        # calculate mass fractions

        abar = 1.0 / np.sum(sdata.X / data.A[:,None], axis = 0)
        zbar = abar *  np.sum(data.Z[:,None] / data.A[:,None] * 
                              sdata.X , axis = 0)
        sdata.abar = abar
        sdata.zbar = zbar

    else:

        if data.A is not None:

            abar = data.A
            zbar = data.Z
            
        else:
            # assume CO
            abar = 96.0/7.0
            zbar = 48.0/7.0

        sdata.abar = abar * np.ones_like(data.x1)
        sdata.zbar = zbar * np.ones_like(data.x1)

    # guess for temp
    tguess = weightedavg_2d(data.T, dm,full)

    # call eos to derive temperature, entropy, etc
    H = helmholtz.helmeos_DE(sdata.d, sdata.e, abar, zbar, tguess = tguess) 

    # put eos results
    sdata.T = H.temp
    sdata.s = H.stot

    # rotation data, taken from the equator

    sdata.v3 = weightedavg_2d(data.v3, dm, equatorial)
    sdata.omega = sdata.v3 / sdata.r
    sdata.j  = weightedavg_2d(RR * data.v3, dm, full)

    # mass loss rate through outer boundary
    sdata.mdot = np.sum(data.d * data.v1, axis = 0) * data.x1**2

    # aspect ratio is useful for determining the final state
    pole = 0
    equator = -1

    logr = np.log10(np.flipud(data.x1))
    logdpole = np.flipud(np.log10(data.d[pole,   :].flatten()))
    logdequator = np.log10(data.d[equator,   :])
    
    flogrpole = interp1d(logdpole,logr, bounds_error = False)
    sdata.aspect = np.nan_to_num(np.exp(np.log10(data.x1) - flogrpole(logdequator)))
    return sdata


def threed_to_oned(data):

    sdata = OneD()

    # spherical radius
    sdata.N = data.x1.size
    sdata.r = data.x1

    # cylindrical radius
    RR = np.outer(np.sin(data.x2), data.x1)

    # volume & mass weights
    dV = data.dV1[None,None,:] * data.dV2[None,:,None] * data.dV3[:,None,None]
    dm = data.d * dV

    # enclosed mass (spherical)
    dmr = np.sum(np.sum(dm, axis = 0), axis = 0)
    msun = 2.0e33

    sdata.menc = np.cumsum(dmr) / msun

#    dj = dm * data.v3 * RR

    # internal energy & density
    sdata.e = weightedavg_3d(data.e, dV)
    sdata.d = weightedavg_3d(data.d, dV)

    # calculate abar & zbar
    if data.X is not None: 

        sdata.X = Xweightedavg_3d(data.X, dm)

        # calculate mass fractions

        abar = 1.0 / np.sum(sdata.X / data.A[:,None], axis = 0)
        zbar = abar *  np.sum(data.Z[:,None] / data.A[:,None] * 
                              sdata.X , axis = 0)
        sdata.abar = abar
        sdata.zbar = zbar

    else:

        if data.A is not None:

            abar = data.A
            zbar = data.Z
            
        else:
            # assume CO
            abar = 96.0/7.0
            zbar = 48.0/7.0

        sdata.abar = abar * np.ones_like(data.x1)
        sdata.zbar = zbar * np.ones_like(data.x1)

    # guess for temp
    tguess = weightedavg_3d(data.T, dm)

    # call eos to derive temperature, entropy, etc
    H = helmholtz.helmeos_DE(sdata.d, sdata.e, abar, zbar, tguess = tguess) 

    # put eos results
    sdata.T = H.temp
    sdata.s = H.stot

    # rotation data, taken from the equator

    sdata.v3 = weightedavg_3d(data.v3, dm)
    sdata.omega = sdata.v3 / sdata.r
    sdata.j  = weightedavg_3d(RR * data.v3, dm)

    # mass loss rate through outer boundary
    sdata.mdot = np.sum(np.sum(data.d * data.v1, axis = 0),axis=0) * data.x1**2

    # aspect ratio is useful for determining the final state
    pole = 0
    equator = -1

    return sdata
