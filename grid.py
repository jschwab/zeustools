import numpy as np

class RatioedGrid:
    
    def __init__(self, npts, xmin = 0, xmax = 1, xrat = 1, igrid = 1):
        self.npts = np.cast['int32'](npts)
        self.igrid = np.cast['int32'](igrid)

        self.xmin = np.cast['float64'](xmin)
        self.xmax = np.cast['float64'](xmax)
        self.xrat = np.cast['float64'](xrat)

        self._make_grid()

    def _make_grid(self):
        
        xagrid = np.empty(self.npts, dtype = np.float64)
        xbgrid = np.empty(self.npts, dtype = np.float64)
        dxgrid = np.empty(self.npts, dtype = np.float64)

        xagrid[0] = self.xmin

        if (self.igrid == -1):
            xrat = 1.0/self.xrat
        elif(self.igrid == 1):
            xrat = self.xrat

        if (xrat == 1.0):
            dxgrid[0] = (self.xmax-self.xmin)/np.cast['float64'](self.npts)
        else:
            dxgrid[0] = (self.xmax-self.xmin)*(xrat-1.0)/(xrat**self.npts - 1.0)
            
        for i in range(1,self.npts):
            dxgrid[i] = dxgrid[i-1] * xrat
            xagrid[i] =  xagrid[i-1] + dxgrid[i-1]

        for i in range(self.npts):
            xbgrid[i] = xagrid[i] + 0.5*dxgrid[i]

        self._agrid = xagrid
        self._bgrid = xbgrid
        
        return

    def agrid(self):
        return self._agrid
    def bgrid(self):
        return self._bgrid



class ZeusTile:
    
    def __init__(self,filename):

        self._read_tile(filename)
        self._compute_cartesian_grids()

        return

    def _read_tile(self, filename):

        with open(filename, "r") as tilefile:
            # this is reversed from the fortran b/c in is a reserved word
            self.ni, self.nj, self.nk = np.fromfile(tilefile, dtype="int32", 
                                                    count = 3, sep = " ")

            raw_data= np.genfromtxt(tilefile, 
                                    dtype = ("int32", "float64", "float64", "float64", "float64"),
                                    names = ("idx", "a", "b", "vla", "vlb"))

            self.ii, self.ij, self.ik = np.split(raw_data["idx"],
                                                 [self.ni,
                                                  self.ni+self.nj])

            self.x1a, self.x2a, self.x3a = np.split(raw_data["a"],
                                                    [self.ni,
                                                     self.ni+self.nj])

            self.x1b, self.x2b, self.x3b = np.split(raw_data["b"],
                                                    [self.ni,
                                                     self.ni+self.nj])

            self.vl1a, self.vl2a, self.vl3a = np.split(raw_data["vla"],
                                                    [self.ni,
                                                     self.ni+self.nj])

            self.vl1b, self.vl2b, self.vl3b = np.split(raw_data["vlb"],
                                                    [self.ni,
                                                     self.ni+self.nj])


            return

    def _compute_cartesian_grids(self):
        
        nphi = 2
        phi_grid = RatioedGrid(npts = nphi, xmin = 0, xmax = 2*np.pi, xrat = 1).bgrid()
        self.nk = nphi
        self.vl3 = 2.0 * np.pi / nphi

        # define things on bb grid

        self.xbb = (self.x1b[:,None,None] 
                    * np.sin(self.x2b[None,:,None]) 
                    * np.cos(phi_grid[None,None,:]))

        self.ybb = (self.x1b[:,None,None] 
                    * np.sin(self.x2b[None,:,None])
                    * np.sin(phi_grid[None,None,:]))

        self.zbb = (self.x1b[:,None,None] 
                    * np.cos(self.x2b[None,:,None])
                    * np.ones(nphi)[None,None,:])

        # define things on ab grid

        self.xab = (self.x1a[:,None,None] 
                    * np.sin(self.x2b[None,:,None]) 
                    * np.cos(phi_grid[None,None,:]))

        self.yab = (self.x1a[:,None,None] 
                    * np.sin(self.x2b[None,:,None])
                    * np.sin(phi_grid[None,None,:]))

        self.zab = (self.x1a[:,None,None] 
                    * np.cos(self.x2b[None,:,None])
                    * np.ones(nphi)[None,None,:])

        # define things on ba grid

        self.xba = (self.x1b[:,None,None] 
                    * np.sin(self.x2a[None,:,None]) 
                    * np.cos(phi_grid[None,None,:]))

        self.yba = (self.x1b[:,None,None] 
                    * np.sin(self.x2a[None,:,None])
                    * np.sin(phi_grid[None,None,:]))

        self.zba = (self.x1b[:,None,None] 
                    * np.cos(self.x2a[None,:,None])
                    * np.ones(nphi)[None,None,:])

        return
