from pydiva import pydiva2d
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import calendar as cl
import time 

#this program creates temp and sal nc files for 10 days a time
#dd from yyyymmdd helps to choose the correct 10 days period

starttime = time.time()

if len(sys.argv) != 5:
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('USAGE: args: \n <dir path containing years> <yyyymmdd> <invalid str> <path to input file>')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('input file shd have coast.cont.* files, coast.depth file and param.par file')
    quit()


invalue = sys.argv[3]    #invalid value (string)
#make ip, op paths, file paths, then send to loop

date = sys.argv[2]
path = sys.argv[1]+'/'+date[0:4]+'/'+date[4:6]
day  = int(date[6:8])

if day >= 1 and day <= 10 :
    path = path+'/1-10'
elif day >= 11 and day <= 20:
    path = path+'/11-20'
elif day >= 21:
    path = path+'/21-'+str(cl.monthrange(int(date[0:4]), int(date[4:6]))[1])

#contourfile = sys.argv[4]+'/input/coast.cont' #initialized this later
paramfile   = sys.argv[4]+'/input/param.par'

outputdir   = sys.argv[4]+'/output'

if not os.path.exists(outputdir):
    os.mkdir(outputdir)


################## function started here #####################

def DIVA(datafile, coastfile, paramfile, outputfile):
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(datafile)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    
    divadir = '/home/darkrai/incois/DIVA/DIVA-4.7.2'

    if not os.path.isdir('output'):
        os.mkdir('output')

    results = pydiva2d.Diva2DResults().make(divadir, datafile=datafile,\
            contourfile=coastfile, paramfile=paramfile, outputfile=outputfile)

################# function ends here ###########################


#splitting file into temp and sal files

for file in os.listdir(path):
    f = open(path+'/'+file, 'r')
    dep = file.split('m')[0][2:]
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

    exten = 999

    depfile = sys.argv[4]+'/input/contour.depth'
    with open(depfile, 'r') as depfile:
        for lno,data in enumerate(depfile, 1):
            if dep == data[:-1]:
                exten = format(lno, '02d')
                break

    if exten == 999:
        print('contour file for',dep,'mts depth doesnt exist, using 0mts contour file instead')
        contourfile = sys.argv[4]+'/input/coast.cont'
    else :
        contourfile = sys.argv[4]+'/input/coast.cont.100'+exten

    DIVA(temfile, contourfile, paramfile, outputdir+'/temp'+dep+'mts_results.nc')
    DIVA(salfile, contourfile, paramfile, outputdir+'/sal'+dep+'mts_results.nc')

    try :
        os.remove(temfile)
        os.remove(salfile)
    except :
        pass

endtime = time.time() 

print('elapsed time :', endtime - starttime)

