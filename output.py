import glob
import h5py
import numpy as np
import os

# define a norm function
    


class ZeusMPOutput:

    def __init__(self, datadir = "./"):
        self.datadir = datadir
        self.hdf5_files = glob.glob(os.path.join(datadir, "hdfaa.*"))
        
        self.times = []
        for hfile in self.hdf5_files:
            with h5py.File(hfile) as h:
                print(h.items())
                self.times.append(h['   time'][0])
        self.times = np.array(self.times, dtype = "float64")

    def compare(self, anotherZMPOutput):
        pass

    def showtimes(self):
        return self.times

