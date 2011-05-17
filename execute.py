import glob
import os
import re
import shlex
import shutil
import subprocess
import sys

class ZeusMP:

    def __init__(self, zeus_config):
        self.zeusdir = zeus_config.get("Directories", "rootdir")
        self.exedir =  zeus_config.get("Directories", "exedir")
        self.srcdir =  zeus_config.get("Directories", "srcdir")
        self.makefile= zeus_config.get("Compilation", "Makefile")
        self.mpiexec = zeus_config.get("Execution",   "mpiexec")

        self.fullexedir = os.path.join(self.zeusdir, self.exedir)
        self.fullsrcdir = os.path.join(self.zeusdir, self.srcdir)

    def run(self, nproc = 1):
        """Run ZEUS-MP2 and post-process the output"""

        fstdout = open(os.path.join(self.fullexedir, "zmp.stdout"), 'w')

        try:
            # construct command
            zmp_exe = os.path.join(self.fullexedir,"zeusmp.x")
            zmp = shlex.split("{} -n {} {}".format(self.mpiexec, nproc, zmp_exe))

            subprocess.check_call(zmp, stdout = fstdout, cwd = self.fullexedir)

        except (OSError, subprocess.CalledProcessError):

            print("Running Zeus Failed")
            print("Terminating...")
            sys.exit(-1)

        fstdout.close()

        try:
            # run included post-processing routine
            pp = subprocess.Popen(os.path.join(self.fullexedir, "zmp_pp.x"),
                                  cwd = self.fullexedir,
                                  stdin  = subprocess.PIPE, 
                                  stdout = subprocess.PIPE)
        except:
            pass
        
        nfiles = len(glob.glob(os.path.join(self.fullexedir, "hdfaa000000.*"))) - 1
        pp.communicate(input="auto_h5\n0\n{}\nquit\n".format(nfiles))

        return 

    def clean(self):
        """Run make clean"""

        make_clean = "make -f {} clean".format(self.makefile)
        subprocess.check_call(shlex.split(make_clean), stdout = subprocess.PIPE,
                              cwd = self.fullsrcdir)

        return

    def newprob(self, probname):
        """Run make newprob and set DPROBLEM=probname"""

        make_newprob = "make -f {} newprob".format(self.makefile)
        subprocess.check_call(shlex.split(make_newprob), stdout = subprocess.PIPE,
                              cwd = self.fullsrcdir)
        
        # read in the makefile
        with open(os.path.join(self.fullsrcdir, self.makefile), "r") as mf:
            lines = mf.readlines()

        # write it back out
        with open(os.path.join(self.fullsrcdir, self.makefile), "w") as mf:
            for line in lines:
                mf.write(re.sub("DPROBLEM=\w*","DPROBLEM={}".format(probname),line))

        return

    def compile(self, newprob = False):
        """ Recompile ZEUS-MP2"""

        make_all = "make -f {} all".format(self.makefile)
        subprocess.check_call(shlex.split(make_all), stdout = subprocess.PIPE,
                              cwd = self.fullsrcdir)

        return


    def archive(self, target_dir):
        
        def archive_file(filename, target_dir):
            return os.rename(os.path.join(self.zeusdir,self.exedir,filename), 
                             os.path.join(target_dir, filename))



        try:
            os.mkdir(target_dir)
        except OSError:
            shutil.rmtree(target_dir)
            os.mkdir(target_dir)

        hdf_files = glob.glob(os.path.join(self.fullexedir, "hdfaa.*"))
        for hdf_file in hdf_files:
            hdf_filename = os.path.split(hdf_file)[1]
            archive_file(hdf_filename, target_dir)
                
        for filename in ["zmp_log", "zmp_inp", "zmp.stdout"]:
            archive_file(filename, target_dir)

        pre_files = glob.glob(os.path.join(self.fullexedir,"hdfaa*.*"))
        for pre_file in pre_files:
            os.remove(pre_file)

        return


if __name__ == "__main__":
    pass
