from collections import OrderedDict
import copy
import os

class ZeusMPInput:
    """Write and manipulate zmp_inp files"""

### BEGIN ZEUS-MP2 NAMELIST TEMPLATE ###
### see http://lca.ucsd.edu/portal/codes/zeusmp2/configuring for explanation of the parameters ###

    _namelists_default = OrderedDict([

    ("geomconf" , OrderedDict([
         ("lgeom"  ,  1),
         ("ldimen" ,  1)      ])),

    ("physconf",  OrderedDict([
         ("lrad"     , 0    ),
         ("leos"     , 1    ),
         ("nspec"    , None ),
         ("xhydro"   , True ),
         ("xforce"   , True ),
         ("xmhd"     , False), 
         ("xtotnrg"  , False), 
         ("xgrav"    , False),  
         ("xgrvfft"  , False), 
         ("xptmass"  , False),
         ("xiso"     , False), 
         ("xsubav"   , False),
         ("xvgrid"   , False)  ])),
    
    ("ioconf",    OrderedDict([
         ("xascii"   , False),
         ("xhdf"     , True ),	
         ("xrestart" , False), 
         ("xtsl"     , False)  ])),
    
    ("preconf"  , OrderedDict([
         ("small_no" , "1.0D-99"),
         ("large_no" , "1.0D+99") ])),
    
    ("arrayconf",  OrderedDict([
         ("izones"   , 8 ),
         ("jzones"   , 8 ),
         ("kzones"   , 8 ), 
         ("maxijk"   , 8 )     ])) ,

    ("mpitop"   , OrderedDict([
         ("ntiles(1)"   , 1),
         ("ntiles(2)"   , 1),
         ("ntiles(3)"   , 1),
         ("periodic(1)" , False), 
         ("periodic(2)" , False), 
         ("periodic(3)" , False)  ])), 

    ("rescon"     , OrderedDict([
         ("irestart"   , 0),
         ("resfile"    , None),
                                ])),

    ("pcon"     , OrderedDict([
         ("nlim",   100000), 
         ("tlim",   0.0   ), 
         ("cpulim", 100000.0), 
         ("mbatch", 1)         ])),

    ("hycon"    , OrderedDict([
         ("qcon"   , 2.0),
         ("qlin"   , None),
         ("courno" , 0.5)     ])),

    ("iib"      ,OrderedDict([
         ("niis(1)" , 1) ,
         ("niis(2)" , None) ,
         ("niis(3)" , None) ,
         ("fiis(1)" , None) ,
         ("fiis(2)" , None) ,
         ("fiis(3)" , None) ,
         ("fiis(4)" , None) ,
         ("fiis(5)" , None) ,
         ("fiis(6)" , None) ,
         ("fiis(7)" , None) ,
         ("fiis(8)" , None) ,
         ("fiis(9)" , None) ,
         ("fiis(10)" , None) ,
         ("fiis(11)" , None) ,
         ("fiis(12)" , None) ,
         ("fiis(13)" , None) ])),

    ("oib"      ,OrderedDict([
         ("nois(1)" , 1) ,
         ("nois(2)" , None) ,
         ("nois(3)" , None) ,
         ("fois(1)" , None) ,
         ("fois(2)" , None) ,
         ("fois(3)" , None) ,
         ("fois(4)" , None) ,
         ("fois(5)" , None) ,
         ("fois(6)" , None) ,
         ("fois(7)" , None) ,
         ("fois(8)" , None) ,
         ("fois(9)" , None) ,
         ("fois(10)" , None) ,
         ("fois(11)" , None) ,
         ("fois(12)" , None) ,
         ("fois(13)" , None) ])),

    ("ijb"      ,OrderedDict([
         ("nijs(1)" , 1) ,
         ("nijs(2)" , None) ,
         ("nijs(3)" , None) ,
         ("fijs(1)" , None) ,
         ("fijs(2)" , None) ,
         ("fijs(3)" , None) ,
         ("fijs(4)" , None) ,
         ("fijs(5)" , None) ,
         ("fijs(6)" , None) ,
         ("fijs(7)" , None) ,
         ("fijs(8)" , None) ,
         ("fijs(9)" , None) ,
         ("fijs(10)" , None) ,
         ("fijs(11)" , None) ,
         ("fijs(12)" , None) ,
         ("fijs(13)" , None) ])),

    ("ojb"      ,OrderedDict([
         ("nojs(1)" , 1) ,
         ("nojs(2)" , None) ,
         ("nojs(3)" , None) ,
         ("fojs(1)" , None) ,
         ("fojs(2)" , None) ,
         ("fojs(3)" , None) ,
         ("fojs(4)" , None) ,
         ("fojs(5)" , None) ,
         ("fojs(6)" , None) ,
         ("fojs(7)" , None) ,
         ("fojs(8)" , None) ,
         ("fojs(9)" , None) ,
         ("fojs(10)" , None) ,
         ("fojs(11)" , None) ,
         ("fojs(12)" , None) ,
         ("fojs(13)" , None) ])),

    ("ikb"      ,OrderedDict([
         ("niks(1)" , 1) ,
         ("niks(2)" , None) ,
         ("niks(3)" , None) ,
         ("fiks(1)" , None) ,
         ("fiks(2)" , None) ,
         ("fiks(3)" , None) ,
         ("fiks(4)" , None) ,
         ("fiks(5)" , None) ,
         ("fiks(6)" , None) ,
         ("fiks(7)" , None) ,
         ("fiks(8)" , None) ,
         ("fiks(9)" , None) ,
         ("fiks(10)" , None) ,
         ("fiks(11)" , None) ,
         ("fiks(12)" , None) ,
         ("fiks(13)" , None) ])),

    ("okb"      ,OrderedDict([
         ("noks(1)" , 1) ,
         ("noks(2)" , None) ,
         ("noks(3)" , None) ,
         ("foks(1)" , None) ,
         ("foks(2)" , None) ,
         ("foks(3)" , None) ,
         ("foks(4)" , None) ,
         ("foks(5)" , None) ,
         ("foks(6)" , None) ,
         ("foks(7)" , None) ,
         ("foks(8)" , None) ,
         ("foks(9)" , None) ,
         ("foks(10)" , None) ,
         ("foks(11)" , None) ,
         ("foks(12)" , None) ,
         ("foks(13)" , None) ])),

    ("ggen1"    , []  ),

    ("ggen2"    , []  ),

    ("ggen3"    , []  ),

    ("grvcon"   , OrderedDict([
         ("guniv"  ,None),   
         ("tgrav"  ,None),
         ("ptmass" ,None),
         ("x1ptm"  ,None),
         ("x2ptm"  ,None),
         ("x3ptm"  ,None),
         ("xwedge" ,None)     ])),


    ("radcon"   , OrderedDict([
        ("fld",         None),
        ("epsme",       None),
        ("cnvcrit",     None),
        ("ernom",       None),
        ("ennom",       None),
        ("demax",       None),
        ("dermax",      None),
        ("nmeiter",     None),
        ("radth	",      None),
        ("epsmaxd",     None),
        ("cgerrcrit",   None),
        ("ipcflag",     None),
        ("xnu",         None),
        ("powr",        None),
        ("rho0",        None),
        ("t_0",         None),
        ("rmfp0",       None) ])),

    ("eqos"     , OrderedDict([
         ("gamma" , 5.0/3.0),
         ("mmw"   , None)        ])),

    ("pgen"     , OrderedDict([
                              ])),

    ("gcon"     , OrderedDict([
                              ])),

    ("iocon"    , OrderedDict([
         ("tusr",  0.0), 
         ("dtusr", 1.0),
         ("thdf",  0.0),
         ("dthdf", 1.0)    ]))

    ])  

### END ZEUS-MP2 NAMELIST TEMPLATE ###


    def __init__(self):
        self._namelists = copy.deepcopy(self._namelists_default)

    def set_value(self, namelist, option, value):
        try:
            self._namelists[namelist][option] = value
        except KeyError:
            pass
        
        return

    def get_value(self, namelist, option):
        try:
            retval = self._namelists[namelist][option]
        except KeyError:
            pass
        
        return retval


    def set_geometry(self, lgeom = None, ldimen = None):
        """Set coordinate system and number of dimensions"""
        if lgeom:  self.set_value("geomconf" , "lgeom"  , lgeom)
        if ldimen: self.set_value("geomconf" , "ldimen" , ldimen)
        return

    def set_eos(self, leos = 1):
        self.set_value("physconf", "leos", leos)
        return

    def set_nzones(self, izones = 1, jzones = 1, kzones = 1):
        """Set number of zones on each tile"""
        self.set_value("arrayconf", "izones", izones)
        self.set_value("arrayconf", "jzones", jzones)
        self.set_value("arrayconf", "kzones", kzones)
        self.set_value("arrayconf", "maxijk", max([izones, jzones, kzones]))
        return

    def set_ntiles(self, itiles = 1, jtiles = 1, ktiles = 1):
        """Set how many MPI tiles will be used"""
        self.set_value("mpitop", "ntiles(1)", itiles)
        self.set_value("mpitop", "ntiles(2)", jtiles)
        self.set_value("mpitop", "ntiles(3)", ktiles)
        return

    def set_output(self):
        """Choose output format and frequency"""
        return

    def set_mhd_bc(self, iis = None, ois = None , 
                         ijs = None, ojs = None , 
                         iks = None, oks = None):
        """
        Set MHD boundary conditions

        Any of 6 mhd boundary conditions may be specified independently
        at every zone on the physical problem boundary.  The boundary type is
        specified by nflo, where

            nflo = 0  =>  interior boundary (get data from neighboring tile)
                 = 1  =>  reflecting (v(normal) = b(normal) = 0)
                 =-1  =>  reflecting (XYZ: same as 1; ZRP: same as 1 with
                          inversion of 3-components at ijb; RTP: same as 1
                          with inversion of 2- and 3-components at iib and
                          inversion of 3-components at ijb and ojb.)
                 = 2  =>  flow out
                 = 3  =>  flow in
                 = 4  =>  periodic
                 = 5  =>  reflecting (v(normal) = 0, b(tangential) = 0)

        Note that in ZRP and RTP, some boundary conditions are implied by
        the choice of limits.  e.g., if 0 .le. x3a .le. 2*pi in either ZRP
        or RTP, then periodic boundary conditions should be imposed.
        Set "niib" to -1 (reflecting with inversion of 2- and 3-components) 
        if the inner i boundary is at the   origin (RTP).
        Set "nijb" to -1 (reflecting with inversion of 3-components) if
           the inner j boundary is on the "Z" axis (ZRP or RTP).
        Set "nojb" to -1 (reflecting with inversion of 3-components) if
           the outer j boundary is on the "Z" axis (RTP).
        """

        # set the appropriate boundary flags
        if iis is not None: self.set_value("iib" , "niis(1)" , iis)
        if ois is not None: self.set_value("oib" , "nois(1)" , ois)
        if ijs is not None: self.set_value("ijb" , "nijs(1)" , ijs)
        if ojs is not None: self.set_value("ojb" , "nojs(1)" , ojs)
        if iks is not None: self.set_value("ikb" , "niks(1)" , iks)
        if oks is not None: self.set_value("okb" , "noks(1)" , oks)
        
        # ensure that the appropriate MPI periodicities are set
        if ( (iis == 4) or (ois == 4) ):
            self.set_value("mpitop", "periodic(1)", True)
        if ( (ijs == 4) or (ojs == 4) ):
            self.set_value("mpitop", "periodic(2)", True)
        if ( (iks == 4) or (oks == 4) ):
            self.set_value("mpitop", "periodic(3)", True)
        
        return


    def set_grav_bc(self, iis = None, ois = None , 
                          ijs = None, ojs = None , 
                          iks = None, oks = None):
        """
        Set gravity boundary conditions
        
        Boundary conditions on the gravitational potential are
        specified by igr, where
       
          igr = 0  =>  interior boundary (get data from neighboring tile)
              = 1  =>  reflecting (dgp/d(normal) = 0 "von Neumann")
              = 2  =>  outflow (equivalent to reflecting)
              = 3  =>  gp specified (Dirichlet)
              = 4  =>  periodic
       
        The flags are defined by analogy with the hydro nflo flag.  This
        is quite different from ZEUS-2D.  The flags igr are read in as:
       
         niis(3),nois(3),nijs(3),nojs(3),niks(3),noks(3)
        """

        # set the appropriate boundary flags
        if iis is not None: self.set_value("iib" , "niis(3)" , iis)
        if ois is not None: self.set_value("oib" , "nois(3)" , ois)
        if ijs is not None: self.set_value("ijb" , "nijs(3)" , ijs)
        if ojs is not None: self.set_value("ojb" , "nojs(3)" , ojs)
        if iks is not None: self.set_value("ikb" , "niks(3)" , iks)
        if oks is not None: self.set_value("okb" , "noks(3)" , oks)

        return


    def set_limits(self, nlim = 1000000, tlim = 1.0, cpulim = 3600.0):
        self.set_value("pcon", "nlim", nlim)
        self.set_value("pcon", "tlim", tlim)
        self.set_value("pcon", "cpulim", cpulim)

        return

    def set_grvcon(self, guniv = None, ptmass = None, xptm = (0.0, 0.0, 0.0)):
        if guniv is not None: self.set_value("grvcon", "guniv", guniv)
        if ptmass is not None:
            self.set_value("grvcon", "ptmass", ptmass)
            self.set_value("grvcon", "x1ptm", xptm[0])
            self.set_value("grvcon", "x2ptm", xptm[1])
            self.set_value("grvcon", "x3ptm", xptm[2])
            self.set_value("physconf", "xptmass", True)

        return

    def add_grid(self, axis, nbl = 8, xmin = 0.0, xmax = 1.0, igrid = 1, xrat = None, dxmin = None):
        """Add a grid to the list of ggen# grids"""
        
        s_strs = ["ggen{}", "x{}min", "x{}max", "x{}rat", "dx{}min"]
        s_axis, s_min, s_max, s_rat, s_dmin = [s.format(axis) for s in s_strs]

        for grid in self._namelists[s_axis]:
            grid["lgrid"] = False

        self._namelists[s_axis].append(
            OrderedDict([
                 ("nbl"   , nbl),
                 (s_min   , xmin),
                 (s_max   , xmax),
                 ("igrid" , igrid),
                 (s_rat   , xrat),
                 (s_dmin  , dxmin),
                 ("lgrid" , True)   ])      )

        return


    def set_pgen(self, pdict):
        for k, v in pdict.iteritems():
            self.set_value("pgen", k, v)
        return

    def write(self, location = "./"):

        # how to format the values
        def _fmt_value(val):

            if isinstance(val, bool):
                if val:
                    return ".TRUE."
                else:
                    return ".false."
            elif isinstance(val, float):
                return "{0:22.16E}".format(val)
            else:
                return str(val)


        opt_fmt = "     {0:10} = {1:22}"
        nml_fmt = " &{}\n{}/\n"

        # get zmp file for writing
        with open(os.path.join(location, "zmp_inp"), "w") as zmpfile:
            zmpfile.write(" #### ZEUSMP2 ZMP_INP AUTOGENERATED BY ZEUSTOOLS #### \n")                       

            for namelist, optdict in self._namelists.iteritems():



                if namelist in ["ggen1", "ggen2", "ggen3"]:
                    for grid in optdict:
                        opt_lines = []
                        for option, value in grid.iteritems():
                            if value is not None:
                                opt_lines.append(opt_fmt.format(option, _fmt_value(value)))

                        zmpfile.write(nml_fmt.format(namelist, ",\n".join(opt_lines)))

                else:

                    opt_lines = []
                    for option, value in optdict.iteritems():
                        if value is not None:
                            opt_lines.append(opt_fmt.format(option, _fmt_value(value)))


                    zmpfile.write(nml_fmt.format(namelist, ",\n".join(opt_lines)))
            


if __name__ == "__main__":
    z = ZeusMPInput()
    z.write()
