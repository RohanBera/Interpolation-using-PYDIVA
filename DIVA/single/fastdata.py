from pydiva import pydiva2d
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import time

sttime = time.time()

if len(sys.argv) != 4:
    print('usage: python3 fastdata.py <mld file> <coast file> <param file>')
    quit()

invalue = '9999.000'    #invalid value (string)

f = open(sys.argv[1], 'r')
dep = sys.argv[1].split('/')[-1].split('m')[0][2:]
temfile = 'temp'+dep+'.dat'
salfile = 'sali'+dep+'.dat' 
temp = open(temfile, 'w')
sali = open(salfile, 'w')

for i in f:
    var = i.split()

    if var[2] != invalue:
        temp.write(var[0]+'\t'+var[1]+'\t'+var[2]+'\t1\n')

    if var[3] != invalue:
        sali.write(var[0]+'\t'+var[1]+'\t'+var[3]+'\t1\n')

f.close()
temp.close()
sali.close()


def DIVA(datafile, coastfile, paramfile, outputfile):
    divadir = '/home/darkrai/incois/DIVA/DIVA-4.7.2'

    # Perform the analysis using the specified files
    if not os.path.isdir('output'):
        os.mkdir('output')
        
    results = pydiva2d.Diva2DResults().make(divadir, datafile=datafile,\
            contourfile=coastfile, paramfile=paramfile, outputfile=outputfile)


print('temp.nc file is being created')
DIVA(temfile, sys.argv[2], sys.argv[3], './output/temp'+dep+'mts_results.nc')
print('sal.nc file is being created')
DIVA(salfile, sys.argv[2], sys.argv[3], './output/sal'+dep+'mts_results.nc')

try :
    os.remove(temfile)
    os.remove(salfile)
except:
    pass

entime = time.time()
print('elapsed time = ', entime-sttime)
