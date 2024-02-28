#Section-1: Library import
import os
import sys
try:
    import flopy
except:
    fpth = os.path.abspath(os.path.join("..", ".."))
    sys.path.append(fpth)
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
#random.seed(2)

#Section-2: Define modflow parameters
name = "N5_Model"
mf = flopy.modflow.Modflow(
    modelname=name, exe_name="C:/WRDAPP/mf2005.exe", version="mf2005"
)

nlay, nrow, ncol = 1, 150, 200
delr, delc = 10, 10
top  = 50
delv = 1.0    # layer thickness
botm = 20
sy = 0.1  # specific yield
river_inflow_range = (100, 150)  # Range of river inflow in cubic meters per day
nper = 2
perlen = [1, 365]     # simulation length
nstp = [1, 12]       # number of time steps
steady = [True, False]

dis = flopy.modflow.ModflowDis(mf, nlay=nlay, nrow=nrow, ncol=ncol, delr=delr, delc=delc, top=top, botm=botm, nper=nper,
                                   perlen=perlen, nstp=nstp, steady=steady)
ibound = np.ones((nlay, nrow, ncol), dtype=int)
ibound[:, :, 0] = -1  # constant head boundary at left side
ibound[:, :, -1] = -1  # constant head boundary at right side
strt = np.ones((nlay, nrow, ncol), dtype=np.float32) * 100.0
strt[:, :, 0] = 75.0     # left boundary head
strt[:, :, -1] = 75.0     # right boundary head

bas = flopy.modflow.ModflowBas(mf, ibound=ibound, strt=strt)

#Section-3: Plotting and Hydraulic Conductivity Data Visualization

#create the hydraulic conductivity array
hk = np.ones((nlay, nrow, ncol))*13
hk[:, 10, 10] = np.random.lognormal(0,4)
hk[:, 45, 35] = np.random.lognormal(0,4)
hk[:, 60, 40] = np.random.lognormal(0,4)
hk[:, 10, 120] = np.random.lognormal(0,4)
hk[:, 120, 80] = np.random.lognormal(0,4)
hk[:, 145, 150] = np.random.lognormal(0,4)

hk_filtered = np.array([gaussian_filter(hk[i, :, :], sigma=10., order=0) for i in range(nlay)])

im = plt.imshow(hk_filtered[0, :, :])
plt.colorbar(im)
plt.show()

lpf = flopy.modflow.ModflowLpf(mf, hk=hk,sy=sy) #For further MC simulation 