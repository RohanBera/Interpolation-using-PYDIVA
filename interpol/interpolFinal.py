import os 
import sys
import calendar as cl
import numpy as np

if len(sys.argv) != 4:
    print("usage : python3 interpol.py <argo core> <argo obs file> <path where you want to create the dirs>")
    quit()

path = sys.argv[3]

standep = []

with open('contour.depth', 'r') as f:
    for i in f:
        standep.append(int(i))

#standep = [0, 10, 20, 30, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]

#opening files here as later the path will change
f  = open(sys.argv[1], 'r')
#f2 = open('ARGO_Observations_1999_2019.txt', 'r')
f2 = open(sys.argv[2], 'r')

try :
    os.chdir(path)
except:
    os.mkdir(path)
    os.chdir(path)
    
#    print('path doesnt exist')
#    quit()


#fixing the year
year = '2018'

#changing/ making directory for year
try :
    os.chdir(year)
except :
    os.mkdir(year)
    os.chdir(year)

#finding lat long here
colnames = f2.readline()   #we wont be using this line
lonlat = {}             #a dictionary that will store the lon lat 
for line in f2 :
    var = line.split(',')
    if var[0].split('_')[1].split('-')[0] == year :
        lonlat[var[0]] = format(float(var[3]), '.2f')+'\t'+format(float(var[2]), '.2f')

f2.close()


#0 = ARGO_OBSERVATION_ID,
#1 = PRESSURE, 2 = PRESSURE_FLAG, 3 = PRESSURE_ADJ, 4 = PRESSURE_ADJ_FLAG,
#5 = TEMPERATURE,6 = TEMPERATURE_FLAG,7 = TEMPERATURE_ADJ, 8 = TEMPERATURE_ADJ_FLAG,
#9 = SALINITY, 10 = SALINITY_FLAG, 11 = SALINITY_ADJ, 12 = SALINITY_ADJ_FLAG,
#13 = DENSITY, 14 = DENSITY_FLAG, 15 = DENSITY_ADJ, 16 = DENSITY_ADJ_FLAG

#not using this as clmnname changes in the o/p files
colnames = f.readline()  
#we wont be using this line either, for ease of use in following programmes
colname = 'ARGO_OBSERVATION_ID,PRESSURE,TEMPERATURE,SALINITY,ARGO_POSITION_LATITUDE,ARGO_POSITION_LONGITUDE\n'

dep = []
tem = []
sal = []

l = f.readline()
var = l.split(',')

dep.append(float(var[1]))
tem.append(float(var[5]))
sal.append(float(var[9]))

wid = int(var[0].split('_')[0])
date= var[0].split('_')[1]

for i in f:
    row = i
    var = row.split(',')

    owid = wid
    dval = float(var[1])
    tval = float(var[5])
    sval = float(var[9])
    wid  = int(var[0].split('_')[0])

    date = var[0].split('_')[1]
    month = date.split('-')[1]
    day = date.split('-')[2]


##path is created here

    try :
        os.chdir(month)
    except :
        os.mkdir(month)
        os.chdir(month)

    if int(day) >= 1 and int(day) <= 10:
        dirname = '1-10'

    elif int(day) >= 11 and int(day) <= 20:
        dirname = '11-20'

    else :
        enddate = str(cl.monthrange(int(year), int(month))[1])
        dirname = '21-'+enddate

    try :
        os.chdir(dirname)
    except :
        os.mkdir(dirname)
        os.chdir(dirname)

#looping for all line having same wmoid
    while wid == owid:
        if (dval != -9999):
            dep.append(dval)
            tem.append(tval)
            sal.append(sval)

        l = f.readline()
        if l == '':
            break

        var = l.split(',')
    
        owid = wid
        dval = float(var[1])
        tval = float(var[5])
        sval = float(var[9])
        wid  = int(var[0].split('_')[0])

#interpolating (for same wmoid and same date)

    stantem = np.interp(standep, dep, tem, left = 9999, right = 9999)
    stansal = np.interp(standep, dep, sal, left = 9999, right = 9999)

### output ###

#output file will be of the form :
#    <lon> <lat> <temperature> <pressure>
#    the values will be tab delimited
#    lon lat rounded off to 2 decimals
#    temp and sal values rounded off 3 decimals
#    file are stored in the dir mentioned by the user
#    file names will be of the form
#    dp<depth>mts.dat

    
    for i in range(len(standep)):
        filename = 'dp'+str(standep[i])+'mts.dat'
        txt = open(filename, 'a')
#        if os.stat(filename).st_size == 0:

        aoi = str(owid)+'_'+date    #argo observation id
#this unique id is required to extract latlon 

        try :
            txt.write(lonlat[aoi]+'\t'+format(stantem[i],'.3f')+'\t'+format(stansal[i],'.3f')+'\n')
        except :
            txt.write('xxxx\txxxx\t'+format(stantem[i],'.3f')+'\t'+format(stansal[i],'.3f')+'\n')

        txt.close()

    dep = []
    tem = []
    sal = []

    dep.append(dval)
    tem.append(tval)
    sal.append(sval)

    os.chdir('../..')

f.close()
