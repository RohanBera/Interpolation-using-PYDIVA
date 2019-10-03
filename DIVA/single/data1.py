from pydiva import pydiva2d
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import time

st = time.time()

if len(sys.argv) != 4:
    print('usage: python3 data1.py <mld file> <coast file> <param file>')
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

    DivaDirs = pydiva2d.DivaDirectories(divadir)
    DivaFiles = pydiva2d.Diva2Dfiles(DivaDirs.diva2d )

    # Load parameters
    param = pydiva2d.Diva2DParameters().read_from(paramfile)

    #get a description
    print(':: parameteres ::')
    param.describe()
    print()

    xo = param.xori
    xe = param.xend
    yo = param.yori
    ye = param.yend

    # Create projection ( basemap )
    m = Basemap(projection='merc', llcrnrlon = xo ,llcrnrlat = yo,\
        urcrnrlon = xe , urcrnrlat = ye ,resolution ='i')

    # Load data
    data = pydiva2d.Diva2DData()
    data.read_from(datafile)

    # Make a plot
    fig = plt.figure()

    ax = fig.add_axes([xo, yo, xe, ye])
    ax = plt.subplot (111)
    m.ax = ax

    #we get the map here
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    m.drawparallels(np.linspace(yo, ye, 4), labels = [1,0,0,0])#, linewidth=0.2)
    m.drawmeridians(np.linspace(xo, xe, 4), lables = [0,0,0,1])#, linewidth=0.2)

    dataplot = data.add_to_plot(m=m, s=10)

    #### contours ####

    # Load the contours from file
    contour = pydiva2d.Diva2DContours()
    contour.read_from(coastfile)

    # Add to plot
    contour.add_to_plot(m=m, linewidth =3)

    #### mesh ####

    # Read mesh files

    mesh = pydiva2d.Diva2DMesh()
    mesh.make(divadir, contourfile=coastfile, paramfile=paramfile)
    mesh.read_from(DivaFiles.mesh, DivaFiles.meshtopo)

    # Get a description
    print(':: mesh topo ::')
    mesh.describe()
    print()

    # Add to plot
    mesh.add_to_plot(m, linewidth =0.25 ,color ='k')


    #### analysis ####

    # Perform the analysis using the specified files
    try:
        results = pydiva2d.Diva2DResults().make(divadir, datafile=datafile,\
                contourfile=coastfile, paramfile=paramfile, outputfile=outputfile)
    except:
        #creating output dir
        os.mkdir('output')
        results = pydiva2d.Diva2DResults().make(divadir, datafile=datafile,\
                contourfile=coastfile, paramfile=paramfile, outputfile=outputfile)


    # Add results to plot
    resultplot = results.add_to_plot(field ='analysis', m=m)


    #### error ####

    # Add the error field
    #errorplot = results.add_to_plot(field ='error', m=m, cmap =plt.cm.hot_r)

    plt.colorbar(dataplot)
    plt.show()

DIVA(temfile, sys.argv[2], sys.argv[3], './output/temp'+dep+'mts_results.nc')
DIVA(salfile, sys.argv[2], sys.argv[3], './output/sal'+dep+'mts_results.nc')

try :
    os.remove(temfile)
    os.remove(salfile)
except:
    pass

et = time.time()
print('elapsed time = ', et-st)
